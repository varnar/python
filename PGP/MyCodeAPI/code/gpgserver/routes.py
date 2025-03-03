from flask import Flask, request, jsonify,copy_current_request_context
from functions import put_key, get_key, delete_key, list_keys, generate_key, encrypt_message, decrypt_message
import threading
import time

app = Flask(__name__)

@app.route("/keys/get/<key_id>", methods=["GET"])
def get_key_api(key_id):
    result = {}

    @copy_current_request_context
    def get_key_thread():
        key = get_key(key_id)
        result["key"] = key

    thread = threading.Thread(target=get_key_thread)
    thread.start()
    thread.join()

    if not result["key"]:
        return jsonify({"error": "Key not found"}), 404
    return jsonify({"key": result["key"]})

@app.route("/keys/generate", methods=["POST"])
def generate_keys():
    result = {}

    @copy_current_request_context
    def generate_keys_thread():
        data = request.get_json()
        overwrite = data.get("overwrite", False)
        # Check if keys already exist
        if not overwrite:
            existing_private_key = get_key(data["name"] + "-private")
            existing_public_key = get_key(data["name"] + "-public")
            if existing_private_key or existing_public_key:
                result["error"] = "Keys already exist"
                result["status_code"] = 409
                return
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
        result["message"] = "Keys generated and stored"
        result["publicKey"] = public_key
        result["status_code"] = 200

    thread = threading.Thread(target=generate_keys_thread)
    thread.start()
    thread.join()

    if "error" in result:
        return jsonify({"error": result["error"]}), result["status_code"]
    return jsonify({"message": result["message"], "publicKey": result["publicKey"]})

@app.route("/keys/list", methods=["GET"])
def list_all_keys():
    result = {}

    @copy_current_request_context
    def list_keys_thread():
        keys, status_code = list_keys()
        result["keys"] = keys
        result["status_code"] = status_code

    thread = threading.Thread(target=list_keys_thread)
    thread.start()
    thread.join()

    if result["status_code"] == 200:
        return jsonify({"keys": result["keys"]}), 200
    else:
        return jsonify({"error": f"Error listing keys: {result['keys']}"}), result["status_code"]

@app.route("/keys/delete/<key_id>", methods=["DELETE"])
def delete_key_api(key_id):
    result = {}

    @copy_current_request_context
    def delete_key_thread():
        data = delete_key(key_id)
        result["data"] = data

    thread = threading.Thread(target=delete_key_thread)
    thread.start()
    thread.join()

    if not result["data"]:
        return jsonify({"error": "Key not found", "key_id": key_id}), 404
    return jsonify({"message": "Key deleted", "data": result["data"]})

@app.route("/encrypt", methods=["POST"])
def encrypt_api():
    result = {}

    @copy_current_request_context
    def encrypt_thread():
        data = request.get_json()
        public_key = get_key(data["id"] + "-public")
        if not public_key:
            result["error"] = "Public key not found"
            result["status_code"] = 404
            return
        encrypted_message = encrypt_message(public_key, data["message"])
        result["encrypted_message"] = encrypted_message
        result["status_code"] = 200

    thread = threading.Thread(target=encrypt_thread)
    thread.start()
    thread.join()

    if "error" in result:
        return jsonify({"error": result["error"]}), result["status_code"]
    return jsonify({"encrypted_message": result["encrypted_message"]})

@app.route("/decrypt", methods=["POST"])
def decrypt_api():
    result = {}

    @copy_current_request_context
    def decrypt_thread():
        data = request.get_json()
        private_key = get_key(data["id"] + "-private")
        if not private_key:
            result["error"] = "Private key not found"
            result["status_code"] = 404
            return
        decrypted_message = decrypt_message(private_key, data["passphrase"], data["encrypted_message"])
        result["decrypted_message"] = decrypted_message
        result["status_code"] = 200

    thread = threading.Thread(target=decrypt_thread)
    thread.start()
    thread.join()

    if "error" in result:
        return jsonify({"error": result["error"]}), result["status_code"]
    return jsonify({"decrypted_message": result["decrypted_message"]})
