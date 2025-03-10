# GPG Server API

## Overview
GPG Server is a Flask-based application that provides an API for managing GPG keys and encrypting/decrypting messages. This project allows users to upload, generate, list, and delete GPG keys, as well as encrypt and decrypt messages using those keys.

## Project Structure
```
gpgserver
├── app
│   ├── __init__.py          # Initializes the Flask application
│   ├── routes.py            # Contains API routes for key management
│   └── swagger
│       └── swagger.yaml      # Swagger documentation for the API
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

## Setup Instructions

1. **Clone the Repository**
   ```
   git clone <repository-url>
   cd gpgserver
   ```

2. **Create a Virtual Environment**
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```
   flask run
   ```

   The application will be available at `http://127.0.0.1:5000`.

## API Documentation
The API endpoints are documented in the `app/swagger/swagger.yaml` file. You can use tools like Swagger UI to visualize and interact with the API.

## Usage
- **Get Key**: `GET /keys/get/<key_id>`
- **Upload Key**: `POST /keys/upload`
- **Generate Keys**: `POST /keys/generate`
- **List All Keys**: `GET /keys/list`
- **Delete Key**: `DELETE /keys/delete/<key_id>`
- **Encrypt Message**: `POST /encrypt`
- **Decrypt Message**: `POST /decrypt`
- **Encrypt File**: `POST /encrypt_file`
- **Decrypt File**: `POST /decrypt_file`

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.