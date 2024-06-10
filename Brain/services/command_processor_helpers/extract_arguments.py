import re
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def extract_arguments(command, intent_tag, tokens, pos_tags, entities, intents):
    arguments = {}
    intent = next(intent for intent in intents if intent["tag"] == intent_tag)

    # Fallback to POS tagging if not found in regex
    pos_dict = {token.lower(): tag for token, tag in pos_tags}
    entity_dict = {entity.lower(): label for entity, label in entities}

    for arg in intent.get("arguments", []):
        arg_name = arg["name"]
        arg_types = set(arg["types"])

    if arg_name not in arguments:
        for token in tokens:
            token_lower = token.lower()
            if pos_dict.get(token_lower) in arg_types:
                arguments[arg_name] = token_lower
                tokens.remove(token)
                break

        # Check entities for matching types
        if arg_name not in arguments:
            for entity, label in entity_dict.items():
                if label in arg_types:
                    arguments[arg_name] = entity
                    break
    print(arguments)
    return arguments
