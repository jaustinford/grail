"""
Manage Samba mounts to backend RAID
Volume shares at the application
layer.
"""

import os

import hvault

def mount(vault_token: str):
    """
    Use token to access Samba credentials
    and create a non-persisted mount to
    authorized shares.
    """

    smb_host = "192.168.20.5"
    smb_name = "xcalibr-root"
    smb_user = "arthur"
    smb_auth = "root_rw"
    smb_opts = "uid=0,gid=32600,dir_mode=0770,file_mode=0770,seal,vers=3.1.1"

    if os.environ.get("BACKUP_DISK_MOUNTPOINT") == "/grail-dst":
        mount_dir = "/grail-src"

    elif os.environ.get("BACKUP_DISK_MOUNTPOINT") == "/grail-src":
        mount_dir = "/grail-dst"

    if not os.path.isdir(mount_dir):
        os.makedirs(mount_dir)

    smb_pass = hvault.get_secret(
        vault_token,
        "users/raid_vol/" + smb_auth
    )[smb_auth.upper()]

    os.system(
        "mount \
            --type cifs \
            //" + smb_host + "/" + smb_name + " " + mount_dir + " \
            --options 'username=" + smb_user + ",password=" + smb_pass + "," + smb_opts + "'"
    )

def unmount():
    """
    Unmount temp mount location once
    all SMB tasks have completed.
    """

    if os.environ.get("BACKUP_DISK_MOUNTPOINT") == "/grail-dst":
        mount_dir = "/grail-src"

    elif os.environ.get("BACKUP_DISK_MOUNTPOINT") == "/grail-src":
        mount_dir = "/grail-dst"

    os.system("umount " + mount_dir)
