from flask import Flask
from services.command_processor import command_processor_bp
import sys
import os
import logging
from logging.handlers import RotatingFileHandler

sys.path.append('Brain')

app = Flask(__name__)


# Set up logging
log_file = r'f:\Friday\Brain\data\logs\Server.log'
log_level = logging.DEBUG  # Log everything

# Create a RotatingFileHandler to log messages to a file
handler = RotatingFileHandler(log_file, maxBytes=10000, backupCount=1)
handler.setLevel(log_level)

# Create a Formatter to specify the format of log messages
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the Flask app's logger
app.logger.addHandler(handler)

app.register_blueprint(command_processor_bp, url_prefix='/api')

@app.route('/error')
def generate_error():
    # This route will raise an exception
    raise Exception('This is a test error')

if __name__ == "__main__":
    app.run(port=5000, debug=False)
