"""
Copy all files and directories in
/src-backup-path to /dst-backup-path.
"""
import os
import json

import logs
import clone
import resolve

FILE_PATH       = os.path.abspath(__file__)
SRC_DIRNAME     = os.path.dirname(FILE_PATH)
PROJECT_DIRNAME = os.path.dirname(SRC_DIRNAME)
CONF_DIRNAME    = os.path.join(PROJECT_DIRNAME, "conf")
BACKUPS_FILE    = os.path.join(CONF_DIRNAME, "backups.json")

LOGGER = logs.logging.getLogger(__name__)

def process_backup(backup_target: str):
    """
    Direct the flow along whether
    'backup_target_src_fqdn' has a wildcard.
    """

    backup_target_src_fqdn = "/src-backup-path/" + backup_target
    backup_target_dst_fqdn = "/dst-backup-path/" + backup_target

    if "*" in backup_target_src_fqdn:
        backup_target_fqdns = resolve.wildcards(backup_target_src_fqdn)

    else:
        backup_target_fqdns = [
            (
                backup_target_src_fqdn,
                backup_target_dst_fqdn
            )
        ]

    for backup_target_fqdn in backup_target_fqdns:
        if os.path.isfile(backup_target_fqdn[0]):
            clone.file(
                backup_target_fqdn[0],
                backup_target_fqdn[1]
            )

        elif os.path.isdir(backup_target_fqdn[0]):
            resolve.dirs(backup_target_fqdn[0])

def main():
    """
    Open config and assign elements and
    iterate over 'backup_targets'.
    """

    if os.environ.get("BACKUP_MODE") == "check":
        LOGGER.info("Running in check mode.")

    with open(BACKUPS_FILE, "r", encoding="utf-8") as backups_opened:
        backups_read = backups_opened.read()
        backups_json = json.loads(backups_read)

    for backup_json in backups_json["backups"]:
        if backup_json["name"] == os.environ.get("BACKUP_OBJECT"):
            LOGGER.info("Processing backup : %s", backup_json["name"])

            backup_targets = backup_json["targets"]
            break

    for backup_target in backup_targets:
        process_backup(backup_target)

if __name__ == "__main__":
    main()
