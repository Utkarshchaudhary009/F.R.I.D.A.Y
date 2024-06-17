import keyboard
import time

# Define the functions for key bindings
def search(cmd):
    keyboard.press_and_release('slash')
    keyboard.write(cmd)  # You might want to pass the search term as an argument
    keyboard.press_and_release('enter')

def copy_text():
    keyboard.press_and_release('ctrl+c')

def paste_text():
    keyboard.press_and_release('ctrl+v')

def cut_text():
    keyboard.press_and_release('ctrl+x')

def scroll_up():
    keyboard.press_and_release('page up')

def scroll_down():
    keyboard.press_and_release('page down')

def open_new_tab():
    keyboard.press_and_release('ctrl+t')
    return("Opened a new tab")

def close_tab():
    keyboard.press_and_release('ctrl+w')
    return("Closed the tab")

def navigate_to_url(url):
    keyboard.press_and_release('ctrl+l')
    keyboard.write(url)
    keyboard.press_and_release('enter')
    return(f"Navigated to {url}")

def refresh_page():
    keyboard.press_and_release('ctrl+r')
    return("Refreshed the page")

def open_extension():
    keyboard.press_and_release('ctrl+shift+X')

def open_new_file():
    keyboard.press_and_release('ctrl+n')
    return("Opened a new file")

def save_file():
    keyboard.press_and_release('ctrl+s')
    return("Saved the file")

def close_file():
    keyboard.press_and_release('ctrl+w')
    return("Closed the file")

def comment_code():
    keyboard.press_and_release('ctrl+/')
    return("Commented the code")

def uncomment_code():
    keyboard.press_and_release('ctrl+k, ctrl+u')
    return("Uncommented the code")

def open_terminal():
    keyboard.press_and_release('ctrl+`')
    return("Opened the terminal")

def open_settings():
    keyboard.press_and_release('ctrl+,')
    return("Opened settings")

def undo_action():
    keyboard.press_and_release('ctrl+z')
    return("Undid the action")

def redo_action():
    keyboard.press_and_release('ctrl+y')
    return("Redid the action")

def find_text():
    keyboard.press_and_release('ctrl+f')
    return("Opened find text")

def replace_text():
    keyboard.press_and_release('ctrl+h')
    return("Opened replace text")

def open_dev_tools():
    keyboard.press_and_release('ctrl+shift+i')
    return("Opened Developer Tools")

def close_dev_tools():
    keyboard.press_and_release('ctrl+shift+c')
    return("Closed Developer Tools")

def zoom_in():
    keyboard.press_and_release('ctrl+=')
    return("Zoomed in")

def zoom_out():
    keyboard.press_and_release('ctrl+-')
    return("Zoomed out")

def toggle_full_screen():
    keyboard.press_and_release('F11')
    return("Toggled full screen mode")

# Map commands to functions
command_map = {
    'open new file': open_new_file,
    'save file': save_file,
    'close file': close_file,
    'comment code': comment_code,
    'uncomment code': uncomment_code,
    'open terminal': open_terminal,
    'search': search,
    'copy': copy_text,
    'paste': paste_text,
    'cut': cut_text,
    'scroll up': scroll_up,
    'scroll down': scroll_down,
    'open new tab': open_new_tab,
    'close tab': close_tab,
    'navigate to': navigate_to_url,
    'refresh page': refresh_page,
    'extension': open_extension,
    'setting': open_settings,
    'undo': undo_action,
    'redo': redo_action,
    'find text': find_text,
    'replace text': replace_text,
    'open dev tools': open_dev_tools,
    'close dev tools': close_dev_tools,
    'zoom in': zoom_in,
    'zoom out': zoom_out,
    'full screen': toggle_full_screen,
    'decrease zoom':zoom_out,
    'increase zoom':zoom_in,
}

def key(command):
    # Find the corresponding function for the command and execute it
    for key in command_map:
        if key in command:
            try:
                if 'navigate to' in command:
                    url = command.split('navigate to ')[1]
                    command_map[key](url)
                elif 'search' in command:
                    cmd = command.split('search ')[1]
                    return {"response":command_map[key](cmd)}
                else:
                    command_map[key]()
                return
            except Exception as e:
                return({"response":f"Error executing command '{command}': {e}"})
                return
    return({"response":f"No matching command found for '{command}'"})

# Example usage
# key("open new file")
# time.sleep(5)  # Delay to visually confirm each action
# key("save file")
# time.sleep(2)
if __name__=="__main__": 
    key("open settings")
    key("comment code")
    key("undo action")
    key("redo action")
    key("find text")
    key("replace text")
    key("open dev tools")
    key("close dev tools")
    key("zoom in")
    key("zoom out")
    key("toggle full screen")
