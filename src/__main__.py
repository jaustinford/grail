"""
"""

import os
import re
import json
import shutil
import filecmp

import logs

FILE_PATH       = os.path.abspath(__file__)
SRC_DIRNAME     = os.path.dirname(FILE_PATH)
PROJECT_DIRNAME = os.path.dirname(SRC_DIRNAME)
CONF_DIRNAME    = os.path.join(PROJECT_DIRNAME, "conf")
BACKUPS_FILE    = os.path.join(CONF_DIRNAME, "backups.json")

LOGGER = logs.logging.getLogger(__name__)

LARGE_BINARY_EXTS = [
    "avi", "m4v", "mkv", "mp3",
    "mp4", "mpg", "wav", "webm"
]

def clone_dir(src_dir: str, dst_dir: str):
    """
    """

    dst_relative = re.sub("/dst-backup-path/", "", dst_dir)

    if not os.path.isdir(dst_dir):
        LOGGER.info("Creating dir : %s", dst_relative)

        if os.environ.get("BACKUP_MODE") == "copy":
            os.makedirs(dst_dir)
            shutil.copystat(
                src_dir,
                dst_dir,
                follow_symlinks=False
            )

    else:
        LOGGER.info("Confirmed dir : %s", dst_relative)

def clone_file(src_file: str, dst_file: str):
    """
    """

    should_copy = False

    dst_relative = re.sub("/dst-backup-path/", "", dst_file)

    if not os.path.isfile(dst_file):
        LOGGER.info("Creating file : %s", dst_relative)
        should_copy = True

    else:
        should_compare = True

        for large_binary_ext in LARGE_BINARY_EXTS:
            if src_file.endswith("." + large_binary_ext):
                should_compare = False

        if should_compare:
            if not filecmp.cmp(src_file, dst_file):
                LOGGER.info("Updating standard file : %s", dst_relative)
                should_copy = True

            else:
                LOGGER.info("Confirmed standard file : %s", dst_relative)

        else:
            if os.path.getsize(src_file) != os.path.getsize(dst_file):
                LOGGER.info("Updating large binary file : %s", dst_relative)
                should_copy = True

            else:
                LOGGER.info("Confirmed large binary file : %s", dst_relative)

    if should_copy and os.environ.get("BACKUP_MODE") == "copy":
        shutil.copy2(
            src_file,
            dst_file,
            follow_symlinks=False
        )

def walk_dir(src_dir):
    """
    """

    for walk_roots, walk_dirs, walk_files in os.walk(src_dir):
        clone_dir(
            walk_roots,
            re.sub("/src-backup-path/", "/dst-backup-path/", walk_roots)
        )

        for walk_dir in walk_dirs:
            dir_src_fqdn = os.path.join(walk_roots, walk_dir)
            dir_dst_fqdn = re.sub("/src-backup-path/", "/dst-backup-path/", dir_src_fqdn)

            clone_dir(dir_src_fqdn, dir_dst_fqdn)

        for walk_file in walk_files:
            file_src_fqdn = os.path.join(walk_roots, walk_file)
            file_dst_fqdn = re.sub("/src-backup-path/", "/dst-backup-path/", file_src_fqdn)

            clone_file(file_src_fqdn, file_dst_fqdn)

def process_backup(backup_target: str):
    """
    """

    backup_target_src_fqdn = "/src-backup-path/" + backup_target
    backup_target_dst_fqdn = "/dst-backup-path/" + backup_target

    if os.path.isfile(backup_target_src_fqdn):
        clone_file(
            backup_target_src_fqdn,
            backup_target_dst_fqdn
        )

    elif os.path.isdir(backup_target_src_fqdn):
        walk_dir(backup_target_src_fqdn)

def main():
    """
    """

    with open(BACKUPS_FILE, "r", encoding="utf-8") as backups_opened:
        backups_read = backups_opened.read()
        backups_json = json.loads(backups_read)

    for backup_json in backups_json["backups"]:
        if backup_json["name"] == os.environ.get("BACKUP_OBJECT"):
            backup_targets = backup_json["targets"]
            break

    if os.environ.get("BACKUP_MODE") == "check":
        LOGGER.info("Running in check mode. Nothing will be written.")

    LOGGER.info("Processing backup object : %s", backup_json["name"])

    for backup_target in backup_targets:
        process_backup(backup_target)

if __name__ == "__main__":
    main()
