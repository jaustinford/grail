"""
Manage VeraCrypt encrypted volumes for
both mounting to and unmounting from
the filesystem.
"""

import os

import logs
import hvault

LOGGER = logs.logging.getLogger(__name__)

def mount(vault_token: str, vcrypt_mount:str):
    """
    Mount a VeraCrypt encrypted volume
    and set appropriate symlink.
    """


    disk_password = hvault.get_secret(
        vault_token,
        "disks/raid_vol/backups"
    )[os.environ.get("BACKUP_DISK_NAME")]

    LOGGER.info("Attempting to mount : %s", os.environ.get("BACKUP_DISK_DEVICE"))

    if not os.path.isdir(vcrypt_mount):
        os.makedirs(vcrypt_mount)

    os.system("\
        echo '" + disk_password + "' | veracrypt \
            --text \
            --mount-options=nokernelcrypto \
            --stdin \
            --keyfiles \"\" \
            --pim=0 \
            --non-interactive \
            --protect-hidden=no " + \
            os.environ.get("BACKUP_DISK_DEVICE") + " " + vcrypt_mount
    )

def unmount(vcrypt_mount: str):
    """
    Unmount a VeraCrypt encrypted volume
    and set appropriate symlink.
    """

    LOGGER.info("Attempting to unmount : %s", os.environ.get("BACKUP_DISK_DEVICE"))

    os.system("\
        veracrypt \
            --unmount " + \
            vcrypt_mount
    )
