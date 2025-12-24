"""
Manage Samba mounts to backend RAID
Volume shares at the application
layer.
"""

import os

import logs
import hvault

LOGGER = logs.logging.getLogger(__name__)

SMB_HOST = "192.168.20.5"
SMB_NAME = "xcalibr-root"
SMB_PATH = "root_rw"
SMB_OPTS = "uid=0,gid=32600,dir_mode=0770,file_mode=0770,seal,vers=3.1.1"

def mount(vault_token: str, rsmb_mount: str):
    """
    Use token to access Samba credentials
    and create a non-persisted mount to
    authorized shares.
    """

    if not os.path.isdir(rsmb_mount):
        os.makedirs(rsmb_mount)

    smb_user = hvault.get_secret(
        vault_token,
        "users/raid_vol/" + SMB_PATH
    )["USERNAME"]

    smb_pass = hvault.get_secret(
        vault_token,
        "users/raid_vol/" + SMB_PATH
    )["PASSWORD"]

    LOGGER.info("Attempting to mount : %s", SMB_NAME)

    os.system(
        "mount \
            --type cifs \
            //" + SMB_HOST + "/" + SMB_NAME + " " + rsmb_mount + " \
            --options 'username=" + smb_user + ",password=" + smb_pass + "," + SMB_OPTS + "'"
    )

def unmount(rsmb_mount: str):
    """
    Unmount temp mount location once
    all SMB tasks have completed.
    """

    LOGGER.info("Attempting to unmount : %s", SMB_NAME)

    os.system("umount " + rsmb_mount)
