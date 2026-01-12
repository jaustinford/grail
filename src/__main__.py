"""
Copy all files and directories between
backup sources.
"""

import os
import traceback

import logs
import gbackup
import infra.rsmb

LOGGER = logs.logging.getLogger(__name__)

def main():
    """
    Mount volume, open config and assign
    elements and iterate over 'backup_targets'.
    """

    if os.environ.get("BACKUP_OBJECT").startswith("raidvol"):
        rsmb_mount = gbackup.get_rsmb_mount()

        infra.rsmb.mount(rsmb_mount)

    try:
        gbackup.iterate_objects()

        if os.environ.get("BACKUP_OBJECT").startswith("raidvol"):
            infra.rsmb.unmount(rsmb_mount)

    except Exception as broad_exception: # pylint: disable=broad-exception-caught
        LOGGER.error(broad_exception)
        traceback.print_exc()

        if os.environ.get("BACKUP_OBJECT").startswith("raidvol"):
            infra.rsmb.unmount(rsmb_mount)

if __name__ == "__main__":
    main()
