"""
Store retrieved secrets into constants
which can be used by the rest of the
project.
"""

import socket

import infra.hvault

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
            vault_port
        )
    )

    vault_socket.close()

    if vault_result == 0:
        vault_alive = True

    return vault_alive

if vault_active(infra.hvault.VAULT_HOST, infra.hvault.VAULT_PORT):
    VAULT_TOKEN = infra.hvault.approle_login("grail")

    ROOT_RW      = infra.hvault.get_secret(VAULT_TOKEN, "users/raid/root_rw")
    ROOT_RW_USER = ROOT_RW["USERNAME"]
    ROOT_RW_PASS = ROOT_RW["PASSWORD"]
