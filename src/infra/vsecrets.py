"""
Store retrieved secrets into constants
which can be used by the rest of the
project.
"""

import os
import socket

import infra.hvault

VAULT_HOST = os.environ.get("VAULT_ENDPOINT").split(":")[0]
VAULT_PORT = os.environ.get("VAULT_ENDPOINT").split(":")[1]

def vault_active(vault_host: str, vault_port: str):
    """
    Return true if 'vault_port' is active
    on 'vault_host'.
    """

    vault_alive = False

    vault_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    vault_result = vault_socket.connect_ex(
        (
            vault_host,
            int(vault_port)
        )
    )

    vault_socket.close()

    if vault_result == 0:
        vault_alive = True

    return vault_alive

if vault_active(VAULT_HOST, VAULT_PORT):
    VAULT_TOKEN = infra.hvault.approle_login("grail")

    ROOT_RW      = infra.hvault.get_secret(VAULT_TOKEN, "users/raid/root_rw")
    ROOT_RW_USER = ROOT_RW["USERNAME"]
    ROOT_RW_PASS = ROOT_RW["PASSWORD"]
