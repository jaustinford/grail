"""
Return lists of directories
given a criteria.
"""

import os
import re

import clone

def wildcards(src_fqdn: str):
    """
    Return a list of directories
    fitting a wildcard pattern.
    """

    matched_files = []

    src_parent = os.path.dirname(src_fqdn)
    src_base   = os.path.basename(src_fqdn).replace("*", "")

    for src_parent_dir in os.listdir(src_parent):
        if src_base in src_parent_dir:
            src_parent_dir_fqdn = src_parent + "/" + src_parent_dir

            matched_files.append(
                (
                    src_parent_dir_fqdn,
                    re.sub("/src-backup-path/", "/dst-backup-path/", src_parent_dir_fqdn)
                )
            )

    return matched_files

def dirs(src_dir: str):
    """
    Walk directories and process
    files separate from nested
    directories.
    """

    for walk_roots, walk_dirs, walk_files in os.walk(src_dir):
        clone.dir(
            walk_roots,
            re.sub("/src-backup-path/", "/dst-backup-path/", walk_roots)
        )

        for walk_dir in walk_dirs:
            dir_src_fqdn = os.path.join(walk_roots, walk_dir)
            dir_dst_fqdn = re.sub("/src-backup-path/", "/dst-backup-path/", dir_src_fqdn)

            clone.dir(dir_src_fqdn, dir_dst_fqdn)

        for walk_file in walk_files:
            file_src_fqdn = os.path.join(walk_roots, walk_file)
            file_dst_fqdn = re.sub("/src-backup-path/", "/dst-backup-path/", file_src_fqdn)

            clone.file(file_src_fqdn, file_dst_fqdn)
