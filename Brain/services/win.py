import pygetwindow as gw
import re

def perform_window_action(arguments):
    action = arguments.get("action")
    target = arguments.get("target")
    position = arguments.get("position")
    size = arguments.get("size")

    if not action or not target:
        return {"response": "Please specify the action and the target window."}

    try:
        # Get all windows and find the matching window
        windows = gw.getWindowsWithTitle(target)
        if not windows:
            return {"response": f"No window with title '{target}' found."}
        
        window = windows[0]

        # Perform the specified action
        if action == "minimize":
            window.minimize()
            return {"response": f"The window '{target}' has been minimized."}
        elif action == "maximize":
            window.maximize()
            return {"response": f"The window '{target}' has been maximized."}
        elif action == "restore":
            window.restore()
            return {"response": f"The window '{target}' has been restored."}
        elif action == "close":
            window.close()
            return {"response": f"The window '{target}' has been closed."}
        elif action == "move" and position:
            x, y = map(int, re.findall(r'\d+', position))
            window.moveTo(x, y)
            return {"response": f"The window '{target}' has been moved to ({x}, {y})."}
        elif action == "resize" and size:
            width, height = map(int, re.findall(r'\d+', size))
            window.resizeTo(width, height)
            return {"response": f"The window '{target}' has been resized to ({width}x{height})."}
        else:
            return {"response": "Unsupported window action or missing parameters."}

    except Exception as e:
        return {"response": f"An error occurred while performing the window action: {str(e)}"}
