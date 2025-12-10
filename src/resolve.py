"""
Return lists of directories
given a criteria.
"""

import os
import re

import clone

def manage_wildcards(src_root: str, dst_root: str, src_fq: str):
    """
    Return a list of directories
    fitting a wildcard pattern.
    """

    matched_files = []

    src_parent = os.path.dirname(src_fq)
    src_base   = os.path.basename(src_fq).replace("*", "")

    for src_parent_dir in os.listdir(src_parent):
        if src_parent_dir.startswith(src_base):
            src_parent_dir_fq = src_parent + "/" + src_parent_dir

            matched_files.append(
                (
                    src_parent_dir_fq,
                    re.sub(src_root, dst_root, src_parent_dir_fq)
                )
            )

    return matched_files

def manage_dirs(backup_direction: str, src_root: str, dst_root: str, src_dir: str):
    """
    Walk directories and process
    files separate from nested
    directories.
    """

    for walk_roots, walk_dirs, walk_files in os.walk(src_dir):
        clone.manage_dir(
            backup_direction,
            dst_root,
            walk_roots,
            re.sub(src_root, dst_root, walk_roots)
        )

        for walk_dir in walk_dirs:
            dir_src_fq = os.path.join(walk_roots, walk_dir)
            dir_dst_fq = re.sub(src_root, dst_root, dir_src_fq)

            clone.manage_dir(
                backup_direction,
                dst_root,
                dir_src_fq,
                dir_dst_fq
            )

        for walk_file in walk_files:
            file_src_fq = os.path.join(walk_roots, walk_file)
            file_dst_fq = re.sub(src_root, dst_root, file_src_fq)

            if os.path.isfile(file_src_fq) or os.path.islink(file_src_fq):
                clone.manage_file(
                    backup_direction,
                    dst_root,
                    file_src_fq,
                    file_dst_fq
                )
