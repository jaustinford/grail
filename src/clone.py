"""
Steps to copy file and directory
content and metadata elements.
"""

import os
import re
import shutil
import filecmp

import constants
import logs

LOGGER = logs.logging.getLogger(__name__)

def diff_file(src_file: str, dst_file: str, dst_relative: str, should_copy: bool):
    """
    Use different methods to compare
    files.
    """

    should_compare = True

    for non_checksum_ext in constants.CONFIG_NON_CHECKSUM_EXTS:
        if src_file.endswith("." + non_checksum_ext):
            should_compare = False
            break

    if should_compare:
        if not filecmp.cmp(src_file, dst_file):
            LOGGER.info("Updating checksum of file : %s", dst_relative)
            should_copy = True

        else:
            LOGGER.info("Confirmed checksum of file : %s", dst_relative)

    else:
        if os.path.getsize(src_file) != os.path.getsize(dst_file):
            LOGGER.info("Updating size of file : %s", dst_relative)
            should_copy = True

        else:
            LOGGER.info("Confirmed size of file : %s", dst_relative)

    return should_copy

def manage_dir(backup_direction: str, dst_root, src_dir: str, dst_dir: str):
    """
    Copy directories and preserve
    metadata elements.
    """

    dst_relative = re.sub(dst_root, backup_direction + " - ", dst_dir)

    if backup_direction == "forward":
        if not os.path.isdir(dst_dir):
            LOGGER.info("Creating dir : %s", dst_relative)

            os.makedirs(dst_dir)
            shutil.copystat(
                src_dir,
                dst_dir,
                follow_symlinks=False
            )

        else:
            LOGGER.info("Confirmed dir : %s", dst_relative)

        src_dir_stat     = os.stat(src_dir)
        src_dir_stat_uid = src_dir_stat.st_uid
        src_dir_stat_gid = src_dir_stat.st_gid

        os.chown(dst_dir, src_dir_stat_uid, src_dir_stat_gid)

    elif backup_direction == "reverse":
        if not os.path.isdir(dst_dir):
            LOGGER.info("Removing dir : %s", dst_relative)
            os.rmdir(src_dir)

        else:
            LOGGER.info("Confirmed dir : %s", dst_relative)

def manage_file(backup_direction: str, dst_root, src_file: str, dst_file: str):
    """
    Copy files and preserve
    metadata elements.
    """

    should_copy = False

    dst_relative = re.sub(dst_root, backup_direction + " - ", dst_file)

    if backup_direction == "forward":
        if not os.path.isfile(dst_file):
            LOGGER.info("Creating file : %s", dst_relative)
            should_copy = True

        else:
            should_copy = diff_file(
                src_file,
                dst_file,
                dst_relative,
                should_copy
            )

        if should_copy:
            shutil.copy2(
                src_file,
                dst_file,
                follow_symlinks=False
            )

        src_file_stat     = os.stat(src_file)
        src_file_stat_uid = src_file_stat.st_uid
        src_file_stat_gid = src_file_stat.st_gid

        os.chown(dst_file, src_file_stat_uid, src_file_stat_gid)

    elif backup_direction == "reverse":
        if not os.path.isfile(dst_file):
            LOGGER.info("Removing file : %s", dst_relative)
            os.remove(src_file)

        else:
            LOGGER.info("Confirmed file : %s", dst_relative)
