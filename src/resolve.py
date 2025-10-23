"""
Return lists of directories
given a criteria.
"""

import os
import re

import clone

def manage_wildcards(src_root: str, dst_root: str, src_fqdn: str):
    """
    Return a list of directories
    fitting a wildcard pattern.
    """

    matched_files = []

    src_parent = os.path.dirname(src_fqdn)
    src_base   = os.path.basename(src_fqdn).replace("*", "")

    for src_parent_dir in os.listdir(src_parent):
        if src_parent_dir.startswith(src_base):
            src_parent_dir_fqdn = src_parent + "/" + src_parent_dir

            matched_files.append(
                (
                    src_parent_dir_fqdn,
                    re.sub(src_root, dst_root, src_parent_dir_fqdn)
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
            dir_src_fqdn = os.path.join(walk_roots, walk_dir)
            dir_dst_fqdn = re.sub(src_root, dst_root, dir_src_fqdn)

            clone.manage_dir(
                backup_direction,
                dst_root,
                dir_src_fqdn,
                dir_dst_fqdn
            )

        for walk_file in walk_files:
            file_src_fqdn = os.path.join(walk_roots, walk_file)
            file_dst_fqdn = re.sub(src_root, dst_root, file_src_fqdn)

            clone.manage_file(
                backup_direction,
                dst_root,
                file_src_fqdn,
                file_dst_fqdn
            )
