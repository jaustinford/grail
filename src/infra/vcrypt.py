"""
Manage VeraCrypt encrypted volumes for
both mounting to and unmounting from
the filesystem.
"""

import os

import logs
import infra.vsecrets

LOGGER = logs.logging.getLogger(__name__)

def mount(vcrypt_mount:str):
    """
    Mount a VeraCrypt encrypted volume
    and set appropriate symlink.
    """

    LOGGER.info("Attempting to mount : %s", os.environ.get("BACKUP_DISK_DEVICE"))

    if not os.path.isdir(vcrypt_mount):
        os.makedirs(vcrypt_mount)

    os.system("\
        echo '" + infra.vsecrets.DISK_PASSWORD + "' | veracrypt \
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
