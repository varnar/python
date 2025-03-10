from flask import Flask, request, jsonify, copy_current_request_context
from functions import put_key, get_key, delete_key, list_keys, generate_key, encrypt_message, decrypt_message
import threading
import json
import os
from werkzeug.utils import secure_filename
from flasgger import Swagger

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit file size to 16 MB
UPLOAD_FOLDER = '/home/ubuntu/code/gpgserver/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

swagger = Swagger(app)

@app.route("/keys/get/<key_id>", methods=["GET"])
def get_key_api(key_id):
    """
    Get a key by its ID.
    ---
    parameters:
      - name: key_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Key found
        schema:
          type: object
          properties:
            key:
              type: string
      404:
        description: Key not found
    """
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

@app.route("/keys/upload", methods=["POST"])
def upload_key():
    """
    Upload a new key.
    ---
    parameters:
      - name: key
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            key:
              type: string
            overwrite:
              type: boolean
    responses:
      200:
        description: Key uploaded successfully
      400:
        description: Invalid JSON format provided
      409:
        description: The key already exists
    """
    result = {}

    @copy_current_request_context
    def upload_key_thread():
        data1 = request.get_data().decode('utf-8').strip()
        print(data1)
        try:
            data = request.get_json()
        except Exception as e:
            print(e)
            result["error"] = "Invalid JSON format provided"
            result["status_code"] = 400
            return
        overwrite = data.get("overwrite", False)
        if not overwrite:
            existing_key = get_key(data["name"])
            if existing_key:
                result["error"] = "The key already exist"
                result["status_code"] = 409
                return
        key_name = data["name"]
        key_value = data["key"]
        put_key(key_name, key_value)
        result["message"] = "Key uploaded successfully"
        result["status_code"] = 200

    thread = threading.Thread(target=upload_key_thread)
    thread.start()
    thread.join()

    if "error" in result:
        return jsonify({"error": result["error"]}), result["status_code"]
    return jsonify({"message": result["message"]})

@app.route("/keys/generate", methods=["POST"])
def generate_keys():
    """
    Generate new keys.
    ---
    parameters:
      - name: key
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            email:
              type: string
            passphrase:
              type: string
            algorithm:
              type: string
            key_size:
              type: integer
            expiration:
              type: string
            comment:
              type: string
            overwrite:
              type: boolean
    responses:
      200:
        description: Keys generated and stored
        schema:
          type: object
          properties:
            publicKey:
              type: string
            fingerprint:
              type: string
      409:
        description: Keys already exist
    """
    result = {}

    @copy_current_request_context
    def generate_keys_thread():
        data = request.get_json()
        overwrite = data.get("overwrite", False)
        if not overwrite:
            existing_private_key = get_key(data["name"] + "-private")
            existing_public_key = get_key(data["name"] + "-public")
            if existing_private_key or existing_public_key:
                result["error"] = "Keys already exist"
                result["status_code"] = 409
                return
        private_key, public_key, fingerprint = generate_key(
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
        result["fingerprint"] = fingerprint
        result["status_code"] = 200

    thread = threading.Thread(target=generate_keys_thread)
    thread.start()
    thread.join()

    if "error" in result:
        return jsonify({"error": result["error"]}), result["status_code"]
    return jsonify({"message": result["message"],"publicKey": result["publicKey"],"fingerprint": result["fingerprint"]})

@app.route("/keys/list", methods=["GET"])
def list_all_keys():
    """
    List all keys.
    ---
    responses:
      200:
        description: List of keys
        schema:
          type: object
          properties:
            keys:
              type: array
              items:
                type: string
      500:
        description: Error listing keys
    """
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
    """
    Delete a key by its ID.
    ---
    parameters:
      - name: key_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Key deleted
      404:
        description: Key not found
    """
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

@app.route("/encrypt/message", methods=["POST"])
def encrypt_api():
    """
    Encrypt a message using a public key.
    ---
    parameters:
      - name: key
        in: body
        required: true
        schema:
          type: object
          properties:
            key-id:
              type: string
            message:
              type: string
    responses:
      200:
        description: Encrypted message
        schema:
          type: object
          properties:
            encrypted_message:
              type: string
      404:
        description: Public key not found
    """
    result = {}

    @copy_current_request_context
    def encrypt_thread():
        data = request.get_json()
        public_key = get_key(data["key-id"])
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

@app.route("/decrypt/message", methods=["POST"])
def decrypt_api():
    """
    Decrypt a message using a private key.
    ---
    parameters:
      - name: key
        in: body
        required: true
        schema:
          type: object
          properties:
            key-id:
              type: string
            passphrase:
              type: string
            encrypted_message:
              type: string
    responses:
      200:
        description: Decrypted message
        schema:
          type: object
          properties:
            decrypted_message:
              type: string
      404:
        description: Private key not found
    """
    result = {}

    @copy_current_request_context
    def decrypt_thread():
        data = request.get_json()
        private_key = get_key(data["key-id"])
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

@app.route("/encrypt/file", methods=["POST"])
def encrypt_file_api():
    """
    Encrypt a file using a public key.
    ---
    parameters:
      - name: file
        in: formData
        required: true
        type: file
      - name: id
        in: formData
        required: true
        type: string
    responses:
      200:
        description: Encrypted message
        schema:
          type: object
          properties:
            encrypted_message:
              type: string
      400:
        description: No file part or no selected file
      404:
        description: Public key not found
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        result = {}

        @copy_current_request_context
        def encrypt_file_thread():
            with open(file_path, 'r') as f:
                file_content = f.read()
            public_key = get_key(request.form['id'])
            if not public_key:
                result["error"] = "Public key not found"
                result["status_code"] = 404
                return
            encrypted_message = encrypt_message(public_key, file_content)
            result["encrypted_message"] = encrypted_message
            result["status_code"] = 200

        thread = threading.Thread(target=encrypt_file_thread)
        thread.start()
        thread.join()

        if "error" in result:
            return jsonify({"error": result["error"]}), result["status_code"]
        return jsonify({"encrypted_message": result["encrypted_message"]})

@app.route("/decrypt/file", methods=["POST"])
def decrypt_file_api():
    """
    Decrypt a file using a private key.
    ---
    parameters:
      - name: file
        in: formData
        required: true
        type: file
      - name: id
        in: formData
        required: true
        type: string
      - name: passphrase
        in: formData
        required: true
        type: string
    responses:
      200:
        description: Decrypted message
        schema:
          type: object
          properties:
            decrypted_message:
              type: string
      400:
        description: No file part or no selected file
      404:
        description: Private key not found
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        result = {}
        print(request)
        @copy_current_request_context
        def decrypt_file_thread():
            with open(file_path, 'r') as f:
                encrypted_message = f.read()
            private_key = get_key(request.form['id'])
            if not private_key:
                result["error"] = "Private key not found"
                result["status_code"] = 404
                return
            decrypted_message = decrypt_message(private_key, request.form['passphrase'], encrypted_message)
            result["decrypted_message"] = decrypted_message
            result["status_code"] = 200

        thread = threading.Thread(target=decrypt_file_thread)
        thread.start()
        thread.join()

        if "error" in result:
            return jsonify({"error": result["error"]}), result["status_code"]
        return jsonify({"decrypted_message": result["decrypted_message"]})