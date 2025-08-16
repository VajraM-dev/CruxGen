import hvac
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv("config.env"))

VAULT_ADDR = os.environ.get("VAULT_ADDR")
VAULT_TOKEN = os.environ.get("VAULT_TOKEN")
MOUNT_POINT = os.environ.get("VAULT_MOUNT_POINT")
PATH = os.environ.get("VAULT_PATH")

client = hvac.Client(
    url=os.environ.get('VAULT_ADDR'),
    token=os.environ.get('VAULT_TOKEN'),
)

if not client.is_authenticated():
    raise Exception("Vault authentication failed. Check your token and Vault server status.")
else:
    print("Vault authentication successful.")

read_secret_result = client.secrets.kv.v2.read_secret_version(
            mount_point=MOUNT_POINT,
            path=PATH,
            raise_on_deleted_version=True
        )