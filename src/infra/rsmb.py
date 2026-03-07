"""
Manage Samba mounts to backend RAID
Volume shares at the application
layer.
"""

import os
import subprocess

import logs
import infra.vsecrets

LOGGER = logs.logging.getLogger(__name__)

SMB_HOST = "192.168.20.5"
SMB_NAME = "xcalibr-root"
SMB_OPTS = "uid=32628,gid=32628,dir_mode=0700,file_mode=0600,seal"

def mount(rsmb_mount: str):
    """
    Use token to access Samba credentials
    and create a non-persisted mount to
    authorized shares.
    """

    smb_user = infra.vsecrets.ROOT_RW_USER
    smb_pass = infra.vsecrets.ROOT_RW_PASS

    if not os.path.isdir(rsmb_mount):
        os.makedirs(rsmb_mount)

    LOGGER.info("Attempting to mount : %s", SMB_NAME)

    subprocess.run(
        [
            "mount",
            "--type",
            "cifs",
            "//" + SMB_HOST + "/" + SMB_NAME,
            rsmb_mount,
            "--options",
            "username=" + smb_user + ",password=" + smb_pass + "," + SMB_OPTS

        ],
        capture_output=True,
        text=True,
        check=True,
        timeout=5
    )

def unmount(rsmb_mount: str):
    """
    Unmount temp mount location once
    all SMB tasks have completed.
    """

    if os.path.ismount(rsmb_mount):
        LOGGER.info("Attempting to unmount : %s", SMB_NAME)

        os.system("umount " + rsmb_mount)
