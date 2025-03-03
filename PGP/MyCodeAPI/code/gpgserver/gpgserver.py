from flask import Flask, request, jsonify
import hvac
import pgpy
from datetime import timedelta


VAULT_ADDR = "https://127.0.0.1:8200"
VAULT_TOKEN = "root"
VAULT_PATH = "pgpkeys/"

app = Flask(__name__)
client = hvac.Client(url=VAULT_ADDR, token=VAULT_TOKEN, verify=False )

def put_key(key_id, key):
    client.secrets.kv.v2.create_or_update_secret(path=VAULT_PATH + key_id, secret={"key": key})

def get_key(key_id):
    try:
        response = client.secrets.kv.v2.read_secret_version(path=VAULT_PATH + key_id)
        print(response)
        return response["data"]["data"].get("key")
    except hvac.exceptions.InvalidPath:
        print(f"Key with id {key_id} does not exist.")
        return None

def delete_key(key_id):
    try:
        response = client.secrets.kv.v2.read_secret_version(path=VAULT_PATH + key_id)
        print(response)
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
    response = client.secrets.kv.v2.list_secrets(path=path)
    keys = response["data"].get("keys", [])
    all_keys = []
    for key in keys:
        if key.endswith('/'):
            all_keys.extend(list_keys(path + key))
        else:
            all_keys.append(path + key)
    return all_keys

# generate a new key pair
# name: Name of the key
# email: Email address associated with the key
# passphrase: Passphrase to protect the key
# algorithm: Algorithm to use for key generation (default: RSAEncryptOrSign)
# key_size: Size of the key (default: 2048)
# expiration: Expiration time in days (default: None)
# comment: Comment to associate with the key
# Returns: private_key, public_key
# Example usage:
# import requests
# url = "http://127.0.0.1:8080/keys/generate"
# payload = {
#     "name": "TestNewKey365",
#     "email": "test@example.com",
#     "passphrase": "",
#     "algorithm": "RSAEncryptOrSign",
#     "key_size": 2048,
#     "expiration": 365,
#     "comment": "Test Comment 365",
#     "overwrite": True
# }
# headers = {"content-type": "application/json"}
# response = requests.post(url, json=payload, headers=headers)
# print(response.json())
def generate_key(name, email, passphrase, algorithm="RSAEncryptOrSign", key_size=2048, expiration=None, comment=None):
    print(expiration)
    expiration = timedelta(days=expiration) if expiration else None
    if expiration:
        print(f"Key will expire in {expiration} days")
    else:
        expiration = None
        print("Key will not expire")
    print(f"Key will expire in {expiration} days")

    algo = getattr(pgpy.constants.PubKeyAlgorithm, algorithm, pgpy.constants.PubKeyAlgorithm.RSAEncryptOrSign)
    key = pgpy.PGPKey.new(algo, key_size)
    uid = pgpy.PGPUID.new(name, email=email, comment=comment)
    key.add_uid(uid, usage={pgpy.constants.KeyFlags.Sign, pgpy.constants.KeyFlags.EncryptCommunications}, hash_alg=pgpy.constants.HashAlgorithm.SHA256, ciphers=[pgpy.constants.SymmetricKeyAlgorithm.AES256], compression=[pgpy.constants.CompressionAlgorithm.ZLIB], key_expiration=expiration)
    if not passphrase.isspace:
        print("Passphrase is provided. Protecting ...")
        key.protect(passphrase,pgpy.constants.SymmetricKeyAlgorithm.AES256,pgpy.constants.HashAlgorithm.SHA256)
    else:
        print("The key is not protected with passphrase as it has not been provided")
    with key.unlock(passphrase):
        private_key = str(key)
    public_key = str(key.pubkey)
    return private_key, public_key

# Encrypt a message using the public key
# public_key_str: Public key in string format
# message: Message to encrypt
# Returns: Encrypted message in string format
# Example usage:
# import requests
# url = "http://
#
# payload = {
#     "id": "TestNewKey365",
#     "message": "Hello, this is a test message."
# }
# headers = {"content-type": "application/json"}
# response = requests.post(url, json=payload, headers=headers)
# print(response.json())
def encrypt_message(public_key_str, message):
    public_key, _ = pgpy.PGPKey.from_blob(public_key_str)
    encrypted_message = public_key.encrypt(pgpy.PGPMessage.new(message))
    return str(encrypted_message)
# Decrypt a message using the private key
# private_key_str: Private key in string format
# passphrase: Passphrase to unlock the private key
# encrypted_message_str: Encrypted message in string format
# Returns: Decrypted message in string format
# Example usage:
# import requests
# url = "http://
# payload = {
#     "id": "TestNewKey365",
#     "passphrase": "",
#     "encrypted_message": "-----BEGIN PGP MESSAGE-----\n...\n-----END PGP MESSAGE-----"
# }
# headers = {"content-type": "application/json"}
# response = requests.post(url, json=payload, headers=headers)
# print(response.json())
def decrypt_message(private_key_str, passphrase, encrypted_message_str):
    private_key, _ = pgpy.PGPKey.from_blob(private_key_str)
    with private_key.unlock(passphrase):
        encrypted_message = pgpy.PGPMessage.from_blob(encrypted_message_str)
        decrypted_message = private_key.decrypt(encrypted_message).message
    return decrypted_message




# read content of the key value from Vault by providing the key id
@app.route("/keys/get/<key_id>", methods=["GET"])
def get_key_api(key_id):
    key = get_key(key_id)
    if not key:
        return jsonify({"error": "Key not found"}), 404
    return jsonify({"key": key})

@app.route("/keys/generate", methods=["POST"])
def generate_keys():
    data = request.get_json()
    overwrite = data.get("overwrite", False)
    # Check if keys already exist
    if not overwrite:
        existing_private_key = get_key(data["name"] + "-private")
        existing_public_key = get_key(data["name"] + "-public")
        if existing_private_key or existing_public_key:
            return jsonify({"error": "Keys already exist"}), 409
    # Generate new keys
    private_key, public_key = generate_key(
        name=data["name"], 
        email=data["email"], 
        passphrase=data["passphrase"], 
        algorithm=data.get("algorithm", "RSAEncryptOrSign"), 
        key_size=data.get("key_size", 2048), 
        expiration=data.get("expiration"), 
        comment=data.get("comment")
    )
    put_key(data["name"] + "-private", private_key)
    put_key(data["name"] + "-public", public_key)
    return jsonify({"message": "Keys generated and stored", "publicKey": public_key})

@app.route("/keys/list", methods=["GET"])
def list_all_keys():
    keys = list_keys()
    return jsonify({"keys": keys})

@app.route("/keys/delete/<key_id>", methods=["DELETE"])
def delete_key_api(key_id):
    data=delete_key(key_id)
    print(data)
    if not data:
        return jsonify({"error": "Key not found","key_id":key_id}), 404
    return jsonify({"message": "Key deleted", "data": data})

@app.route("/encrypt", methods=["POST"])
def encrypt_api():
    data = request.get_json()
    public_key = get_key(data["id"] + "-public")
    if not public_key:
        return jsonify({"error": "Public key not found"}), 404
    encrypted_message = encrypt_message(public_key, data["message"])
    return jsonify({"encrypted_message": encrypted_message})

@app.route("/decrypt", methods=["POST"])
def decrypt_api():
    data = request.get_json()
    private_key = get_key(data["id"] + "-private")
    if not private_key:
        return jsonify({"error": "Private key not found"}), 404
    decrypted_message = decrypt_message(private_key, data["passphrase"], data["encrypted_message"])
    return jsonify({"decrypted_message": decrypted_message})

if __name__ == "__main__":
    app.run(port=8080, host='0.0.0.0',debug=True)

