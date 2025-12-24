"""
Copy all files and directories between
backup sources.
"""

import os
import traceback

import logs
import gbackup
import hvault
import vcrypt
import rsmb

LOGGER = logs.logging.getLogger(__name__)

def main():
    """
    Mount volume, open config and assign
    elements and iterate over 'backup_targets'.
    """

    vault_token = hvault.approle_login("grail")

    if os.environ.get("BACKUP_OBJECT").startswith("raidvol"):
        rsmb_mount = gbackup.get_rsmb_mount()
        rsmb.mount(vault_token, rsmb_mount)

    vcrypt_mount = "/grail-disk"
    vcrypt.mount(vault_token, vcrypt_mount)

    try:
        gbackup.iterate_objects()
        vcrypt.unmount(vcrypt_mount)

        if os.environ.get("BACKUP_OBJECT").startswith("raidvol"):
            rsmb.unmount(rsmb_mount)

    except Exception as broad_exception: # pylint: disable=broad-exception-caught
        LOGGER.error(broad_exception)
        traceback.print_exc()

        vcrypt.unmount(vcrypt_mount)

        if os.environ.get("BACKUP_OBJECT").startswith("raidvol"):
            rsmb.unmount(rsmb_mount)

if __name__ == "__main__":
    main()
