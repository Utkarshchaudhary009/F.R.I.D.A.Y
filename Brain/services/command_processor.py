import json
from flask import Blueprint, request, jsonify
from .command_processor.classify_command import classify_command
from .command_processor.execute_function import execute_function

command_processor_bp = Blueprint('command_processor', __name__)

with open('Brain/intents.json') as file:
    intents = json.load(file)["intents"]

@command_processor_bp.route('/process', methods=['POST'])
def process_command():
    command = request.json.get('command')
    intent, arguments = classify_command(command, intents)
    response = execute_function(intent, arguments)
    return jsonify(response), 200
