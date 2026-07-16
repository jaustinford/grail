"""
Copy all files and directories between
backup sources.
"""

import os
import traceback

import constants
import gbackup
import tpl.smb

MAIN_LOG = constants.logging.getLogger(__name__)

def main():
    """
    Mount volume, open config and assign
    elements and iterate over 'backup_targets'.
    """

    if os.environ.get("BACKUP_OBJECT").startswith("raid"):
        smb_mount = gbackup.get_smb_mount()

        tpl.smb.mount(smb_mount)

    try:
        gbackup.iterate_objects()

        if os.environ.get("BACKUP_OBJECT").startswith("raid"):
            tpl.smb.unmount(smb_mount)

    except Exception as broad_exception: # pylint: disable=broad-exception-caught
        MAIN_LOG.error(broad_exception)
        traceback.print_exc()

        if os.environ.get("BACKUP_OBJECT").startswith("raid"):
            tpl.smb.unmount(smb_mount)

if __name__ == "__main__":
    main()
