from flask import Flask
from .services.command_processor import command_processor_bp

app = Flask(__name__)
app.register_blueprint(command_processor_bp, url_prefix='/api')

if __name__ == "__main__":
    app.run(port=5000, debug=True)
