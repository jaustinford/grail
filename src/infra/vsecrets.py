"""
Store retrieved secrets into constants
which can be used by the rest of the
project.
"""

import os

import infra.hvault

VAULT_TOKEN = infra.hvault.approle_login("grail")

ROOT_RW      = infra.hvault.get_secret(VAULT_TOKEN, "users/raid_vol/root_rw")
ROOT_RW_USER = ROOT_RW["USERNAME"]
ROOT_RW_PASS = ROOT_RW["PASSWORD"]

DISK_PASSWORD = \
    infra.hvault.get_secret(VAULT_TOKEN, "disks/raid_vol/backups")[os.environ.get("BACKUP_DISK_NAME")]
