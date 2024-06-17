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
    print("Opened a new tab")

def close_tab():
    keyboard.press_and_release('ctrl+w')
    print("Closed the tab")

def navigate_to_url(url):
    keyboard.press_and_release('ctrl+l')
    keyboard.write(url)
    keyboard.press_and_release('enter')
    print(f"Navigated to {url}")

def refresh_page():
    keyboard.press_and_release('ctrl+r')
    print("Refreshed the page")

def open_extension():
    keyboard.press_and_release('ctrl+shift+X')

def open_new_file():
    keyboard.press_and_release('ctrl+n')
    print("Opened a new file")

def save_file():
    keyboard.press_and_release('ctrl+s')
    print("Saved the file")

def close_file():
    keyboard.press_and_release('ctrl+w')
    print("Closed the file")

def comment_code():
    keyboard.press_and_release('ctrl+/')
    print("Commented the code")

def uncomment_code():
    keyboard.press_and_release('ctrl+k, ctrl+u')
    print("Uncommented the code")

def open_terminal():
    keyboard.press_and_release('ctrl+`')
    print("Opened the terminal")

def open_settings():
    keyboard.press_and_release('ctrl+,')
    print("Opened settings")

def undo_action():
    keyboard.press_and_release('ctrl+z')
    print("Undid the action")

def redo_action():
    keyboard.press_and_release('ctrl+y')
    print("Redid the action")

def find_text():
    keyboard.press_and_release('ctrl+f')
    print("Opened find text")

def replace_text():
    keyboard.press_and_release('ctrl+h')
    print("Opened replace text")

def open_dev_tools():
    keyboard.press_and_release('ctrl+shift+i')
    print("Opened Developer Tools")

def close_dev_tools():
    keyboard.press_and_release('ctrl+shift+c')
    print("Closed Developer Tools")

def zoom_in():
    keyboard.press_and_release('ctrl+=')
    print("Zoomed in")

def zoom_out():
    keyboard.press_and_release('ctrl+-')
    print("Zoomed out")

def toggle_full_screen():
    keyboard.press_and_release('F11')
    print("Toggled full screen mode")

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
    'open extension': open_extension,
    'open settings': open_settings,
    'undo': undo_action,
    'redo': redo_action,
    'find text': find_text,
    'replace text': replace_text,
    'open dev tools': open_dev_tools,
    'close dev tools': close_dev_tools,
    'zoom in': zoom_in,
    'zoom out': zoom_out,
    'full screen': toggle_full_screen,
}

def execute_command(command):
    # Find the corresponding function for the command and execute it
    for key in command_map:
        if key in command:
            try:
                if 'navigate to' in command:
                    url = command.split('navigate to ')[1]
                    command_map[key](url)
                elif 'search' in command:
                    cmd = command.split('search ')[1]
                    command_map[key](cmd)
                else:
                    command_map[key]()
                return
            except Exception as e:
                print(f"Error executing command '{command}': {e}")
                return
    print(f"No matching command found for '{command}'")

# Example usage
# execute_command("open new file")
# time.sleep(5)  # Delay to visually confirm each action
# execute_command("save file")
# time.sleep(2)
if __name__=="__main__": 
    execute_command("open settings")
    execute_command("comment code")
    execute_command("undo action")
    execute_command("redo action")
    execute_command("find text")
    execute_command("replace text")
    execute_command("open dev tools")
    execute_command("close dev tools")
    execute_command("zoom in")
    execute_command("zoom out")
    execute_command("toggle full screen")
