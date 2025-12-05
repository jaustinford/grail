"""
Copy all files and directories between
backup sources.
"""

import os

import constants
import logs
import clone
import resolve

LOGGER = logs.logging.getLogger(__name__)

def manage_crypt(crypt_mode: str):
    """
    Mount a VeraCrypt encrypted volume
    and set appropriate symlink.
    """

    grail_backup_mountpoint = "/grail-disk"

    if crypt_mode == "mount":
        LOGGER.info("Attempting to mount : %s", os.environ.get("BACKUP_DISK"))

        if not os.path.isdir(grail_backup_mountpoint):
            os.makedirs(grail_backup_mountpoint)

        os.system("\
            veracrypt \
                --text \
                --mount-options=nokernelcrypto \
                --password=\"" + os.environ.get("DISK_PASSWORD") + "\" \
                --keyfiles \"\" \
                --pim=0 \
                --protect-hidden=no " + \
                os.environ.get("BACKUP_DISK") + " " + grail_backup_mountpoint
        )

    elif crypt_mode == "unmount":
        LOGGER.info("Attempting to unmount : %s", os.environ.get("BACKUP_DISK"))

        os.system("\
            veracrypt \
                --unmount"
        )

def process_backup(backup_direction: str, backup_target: str):
    """
    Direct the flow along whether
    'backup_target_src_fqdn' has a wildcard.
    """

    if backup_direction == "forward":
        src_root = "/grail-src/"
        dst_root = "/grail-dst/"

    elif backup_direction == "reverse":
        src_root = "/grail-dst/"
        dst_root = "/grail-src/"

    backup_target_src_fqdn = src_root + backup_target
    backup_target_dst_fqdn = dst_root + backup_target

    if "*" in backup_target_src_fqdn:
        backup_target_fqdns = resolve.manage_wildcards(
            src_root,
            dst_root,
            backup_target_src_fqdn
        )

    else:
        backup_target_fqdns = [
            (
                backup_target_src_fqdn,
                backup_target_dst_fqdn
            )
        ]

    for backup_target_fqdn in backup_target_fqdns:
        if os.path.isfile(backup_target_fqdn[0]):
            clone.manage_file(
                backup_direction,
                dst_root,
                backup_target_fqdn[0],
                backup_target_fqdn[1]
            )

        elif os.path.isdir(backup_target_fqdn[0]):
            resolve.manage_dirs(
                backup_direction,
                src_root,
                dst_root,
                backup_target_fqdn[0]
            )

def main():
    """
    Mount volume, open config and assign
    elements and iterate over 'backup_targets'.
    """

    manage_crypt("mount")

    try:
        if not os.path.islink(os.environ.get("DISK_MOUNTPOINT")):
            os.symlink(
                "/grail-disk/" + os.environ.get("BACKUP_OBJECT").split("-")[0],
                os.environ.get("DISK_MOUNTPOINT")
            )

        for backup_object in constants.CONFIG_OBJECTS:
            if backup_object["name"] == os.environ.get("BACKUP_OBJECT"):
                LOGGER.info("Processing backup : %s", backup_object["name"])

                backup_targets = backup_object["targets"]
                break

        for backup_target in backup_targets:
            process_backup("forward", backup_target)
            process_backup("reverse", backup_target)

    except FileExistsError as file_exists_error:
        LOGGER.error(file_exists_error)
        manage_crypt("unmount")

    manage_crypt("unmount")

if __name__ == "__main__":
    main()
