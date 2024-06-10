import keyboard
import time


# Define the functions for key bindings
def search_chatgpt():
    keyboard.press_and_release('slash')
    keyboard.write('')  # You might want to pass the search term as an argument
    keyboard.press_and_release('enter')

def copy_text():
    keyboard.press_and_release('ctrl+c')

def paste_text():
    keyboard.press_and_release('ctrl+v')

def cut_text():
    keyboard.press_and_release('ctrl+x')

def scroll_up():
    keyboard.press_and_release('page up')
# Define the functions for key bindings
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

def scroll_up():
    keyboard.press_and_release('page up')
    print("Scrolled up")

def scroll_down():
    keyboard.press_and_release('page down')
    print("Scrolled down")

def scroll_down():
    keyboard.press_and_release('page down')

def open_extension():
    keyboard.press_and_release('ctrl+shift+X')

# Define the functions for key bindings
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
    print("Opened Chrome settings")

# Map commands to functions
command_map = {
    'open new file': open_new_file,
    'save file': save_file,
    'close file': close_file,
    'comment code': comment_code,
    'uncomment code': uncomment_code,
    'open terminal': open_terminal,
    'search': search_chatgpt,
    'copy': copy_text,
    'paste': paste_text,
    'open setting':open_settings,
    'cut': cut_text,
    'scroll up': scroll_up,
    'scroll down': scroll_down,
    'open extension': open_extension,
    'open new tab': open_new_tab,
    'close tab': close_tab,
    'navigate to': navigate_to_url,
    'refresh page': refresh_page,
    'scroll up': scroll_up,
    'scroll down': scroll_down
}


def execute_command(command):
    # Find the corresponding function for the command and execute it
    for key in command_map:
        if key in command:
            try:
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
execute_command("open setting")
execute_command("comment code")