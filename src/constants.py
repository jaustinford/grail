"""
Open config files and assign as
project variable constants.
"""

import os
import yaml

FILE_PATH       = os.path.abspath(__file__)
SRC_DIRNAME     = os.path.dirname(FILE_PATH)
PROJECT_DIRNAME = os.path.dirname(SRC_DIRNAME)
CONF_DIRNAME    = os.path.join(PROJECT_DIRNAME, "conf")
BACKUPS_FILE    = os.path.join(CONF_DIRNAME, "backups.yaml")

with open(BACKUPS_FILE, "r", encoding="utf-8") as backups_opened:
    backups_json = yaml.safe_load(backups_opened)["backups"]

CONFIG_NON_CHECKSUM_EXTS = backups_json["non_checksum_exts"]
CONFIG_OBJECTS           = backups_json["objects"]
