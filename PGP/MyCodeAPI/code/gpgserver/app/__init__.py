from flask import Flask, send_from_directory
from flasgger import Swagger
import os

def create_app():
    app = Flask(__name__)

    # Swagger configuration
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "GPG Server API",
            "description": "API for managing GPG keys and encrypting/decrypting messages.",
            "version": "1.0.0"
        },
        "host": "localhost:8080",
        "basePath": "/",
        "schemes": [
            "http"
        ]
    }

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }

    swagger = Swagger(app, config=swagger_config, template=swagger_template)

    # Serve the swagger.yaml file
    @app.route('/swagger/swagger.yaml')
    def swagger_yaml():
        return send_from_directory(os.path.join(app.root_path, 'swagger'), 'swagger.yaml')

    # Import routes
    from . import routes

    return app

app = create_app()