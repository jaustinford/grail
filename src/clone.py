"""
Steps to copy file and directory
content and metadata elements.
"""

import os
import re
import shutil
import filecmp

import logs

LARGE_BINARY_EXTS = [
    "avi", "m4v", "mkv", "mp3",
    "mp4", "mpg", "wav", "webm"
]

LOGGER = logs.logging.getLogger(__name__)

def manage_dir(src_dir: str, dst_dir: str):
    """
    Copy directories and preserve
    metadata elements.
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

def manage_file(src_file: str, dst_file: str):
    """
    Copy files and preserve
    metadata elements.
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
