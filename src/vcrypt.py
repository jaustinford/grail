"""
Manage VeraCrypt encrypted volumes for
both mounting to and unmounting from
the filesystem.
"""

import os

import vault
import logs

LOGGER = logs.logging.getLogger(__name__)

def mount():
    """
    Mount a VeraCrypt encrypted volume
    and set appropriate symlink.
    """

    grail_backup_mountpoint = "/grail-disk"

    backup_disk_password = vault.get_secret(
        "grail",
        "disks/raid_vol/backups"
    )[os.environ.get("BACKUP_DISK_NAME")]

    LOGGER.info("Attempting to mount : %s", os.environ.get("BACKUP_DISK_DEVICE"))

    if not os.path.isdir(grail_backup_mountpoint):
        os.makedirs(grail_backup_mountpoint)

    os.system("\
        veracrypt \
            --text \
            --mount-options=nokernelcrypto \
            --password=\'" + backup_disk_password + "\' \
            --keyfiles \"\" \
            --pim=0 \
            --protect-hidden=no " + \
            os.environ.get("BACKUP_DISK_DEVICE") + " " + grail_backup_mountpoint
    )

def unmount():
    """
    Unmount a VeraCrypt encrypted volume
    and set appropriate symlink.
    """

    LOGGER.info("Attempting to unmount : %s", os.environ.get("BACKUP_DISK_DEVICE"))

    os.system("\
        veracrypt \
            --unmount"
    )
