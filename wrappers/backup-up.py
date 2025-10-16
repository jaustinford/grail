"""
Wrap project Docker compose
functionality.
"""

import os

FILE_PATH       = os.path.abspath(__file__)
FILE_DIRNAME    = os.path.dirname(FILE_PATH)
PROJECT_DIRNAME = os.path.dirname(FILE_DIRNAME)
ENV_DIRNAME     = os.path.join(PROJECT_DIRNAME, "env")

os.system(
    "docker compose \
        --profile backup \
        --env-file " + os.path.join(ENV_DIRNAME, ".env-args") + "\
        --env-file " + os.path.join(ENV_DIRNAME, ".env-secrets") + "\
        up"
)
