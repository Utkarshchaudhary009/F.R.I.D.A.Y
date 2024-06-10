import os
import sys
import json
from flask import Blueprint, request, jsonify
# from command_processor_helpers.classify_command import classify_command
# from command_processor_helpers.execute_function import execute_function
from .command_processor_helpers.classify_command import classify_command
from .command_processor_helpers.execute_function import execute_function

# Add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
command_processor_bp = Blueprint('command_processor', __name__)


@command_processor_bp.route('/process', methods=['POST'])
def process_command():
    command = request.json.get('command')
    function, arguments = classify_command(command)
    response = execute_function(function, arguments)
    return jsonify(response)

if __name__ == "__main__":
    while True:
        test_command = input("enter:")
        # function, arguments = classify_command(test_command)
        # print(function, arguments)
        # response = execute_function(function, arguments)
        # print(response)
