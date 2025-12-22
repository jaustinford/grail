"""
Interact with HashiCorp Vault to retrieve
authorized secrets using the AppRole
authentication method.
"""

import json
import hvac

def read_approle(approle_file: str):
    """
    Read the AppRole credentials from a
    local file and return as a JSON
    object.
    """

    with open("/approle/" + approle_file, "r", encoding="utf-8") as approle_opened:
        approle_read = approle_opened.read()
        approle_json = json.loads(approle_read)

    return approle_json

def vault_approle_login(vault_client: hvac.Client, role_id: str, secret_id: str):
    """
    Login to AppRole in Vault using
    retrieved 'role_id' and 'secret_id'.
    """

    client_token = vault_client.auth.approle.login(
        role_id=role_id,
        secret_id=secret_id
    )["auth"]["client_token"]

    return client_token

def get_secret(approle_name: str, secret_path: str):
    """
    Use generated AppRole token to access
    'secret_path' and return the data field.
    """

    vault_url = "http://192.168.40.1:32524"

    vault_unauth_client = hvac.Client(url=vault_url)

    vault_token = vault_approle_login(
        vault_unauth_client,
        read_approle(approle_name + ".json")["role_id"],
        read_approle(approle_name + ".json")["secret_id"]
    )

    vault_auth_client = hvac.Client(
        url=vault_url,
        token=vault_token
    )

    secret_version = vault_auth_client.secrets.kv.v2.read_secret_version(
        mount_point="lab/kv",
        path=secret_path,
        raise_on_deleted_version=True
    )

    return secret_version["data"]["data"]
