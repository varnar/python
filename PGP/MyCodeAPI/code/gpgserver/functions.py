import hvac
import pgpy
from datetime import timedelta
from flask import jsonify

VAULT_ADDR = "https://127.0.0.1:8200"
VAULT_TOKEN = "root"
VAULT_PATH = "pgpkeys/"

client = hvac.Client(url=VAULT_ADDR, token=VAULT_TOKEN, verify=False)

def put_key(key_id, key):
    client.secrets.kv.v2.create_or_update_secret(path=VAULT_PATH + key_id, secret={"key": key})

def get_key(key_id):
    try:
        response = client.secrets.kv.v2.read_secret_version(path=VAULT_PATH + key_id)
        return response["data"]["data"].get("key")
    except hvac.exceptions.InvalidPath:
        print(f"Key with id {key_id} does not exist.")
        return None

def delete_key(key_id):
    try:
        response = client.secrets.kv.v2.read_secret_version(path=VAULT_PATH + key_id)
        # Delete the key
        client.secrets.kv.v2.delete_metadata_and_all_versions(path=VAULT_PATH + key_id)
        print(f"Key with id {key_id} deleted.")
        return response
    except hvac.exceptions.InvalidRequest:
        print(f"Key with id {key_id} does not exist.")
        return None      
    except hvac.exceptions.InvalidPath:
        print(f"Key with id {key_id} does not exist.")
        return None

def list_keys(path=VAULT_PATH):
    try:
        response = client.secrets.kv.v2.list_secrets(path=path)
    except hvac.exceptions.InvalidRequest:
        print(f"Invalid request: {path}")
        return {"error": "Invalid request", "path": path}, 400
    except hvac.exceptions.InvalidPath:
        print(f"Invalid path: {path}")
        return {"error": "Invalid path or no keys under this path", "path": path}, 404
    keys = response["data"].get("keys", [])
    all_keys = []
    for key in keys:
        if key.endswith('/'):
            sub_keys, _ = list_keys(path + key)
            all_keys.extend(sub_keys)
        else:
            all_keys.append(path + key)
    return all_keys, 200

def generate_key(name, email, passphrase, algorithm="RSAEncryptOrSign", key_size=2048, expiration=None, comment=None):
    expiration = timedelta(days=expiration) if expiration else None
    if expiration:
        print(f"Key will expire in {expiration} days")
    else:
        print("Key will not expire")

    algo = getattr(pgpy.constants.PubKeyAlgorithm, algorithm, pgpy.constants.PubKeyAlgorithm.RSAEncryptOrSign)
    key = pgpy.PGPKey.new(algo, key_size)
    uid = pgpy.PGPUID.new(name, email=email, comment=comment)
    key.add_uid(uid, usage={pgpy.constants.KeyFlags.Sign, pgpy.constants.KeyFlags.EncryptCommunications}, hash_alg=pgpy.constants.HashAlgorithm.SHA256, ciphers=[pgpy.constants.SymmetricKeyAlgorithm.AES256], compression=[pgpy.constants.CompressionAlgorithm.ZLIB], key_expiration=expiration)
    if passphrase and not passphrase.isspace():
        print("Passphrase is provided. Protecting ...")
        key.protect(passphrase, pgpy.constants.SymmetricKeyAlgorithm.AES256, pgpy.constants.HashAlgorithm.SHA256)
    else:
        print("The key is not protected with passphrase as it has not been provided")
    with key.unlock(passphrase):
        private_key = str(key)
    public_key = str(key.pubkey)
    return private_key, public_key

def encrypt_message(public_key_str, message):
    public_key, _ = pgpy.PGPKey.from_blob(public_key_str)
    encrypted_message = public_key.encrypt(pgpy.PGPMessage.new(message))
    return str(encrypted_message)

def decrypt_message(private_key_str, passphrase, encrypted_message_str):
    private_key, _ = pgpy.PGPKey.from_blob(private_key_str)
    with private_key.unlock(passphrase):
        encrypted_message = pgpy.PGPMessage.from_blob(encrypted_message_str)
        decrypted_message = private_key.decrypt(encrypted_message).message
    return decrypted_message