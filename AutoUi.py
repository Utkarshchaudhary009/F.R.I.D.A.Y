import pyautogui
import time
from rich.console import Console

# Initialize Console
console = Console()
array=["asks about each others health and good ness","engages in playful teasing and fun conversations.","discusses about there favourites","engages in funny conversation","asks for user feedback and suggestions.","engages in interactive conversation.","act like a friend taking just random thing."]
# Function to automate the described process
def automate_iui():
    for i in array:
        # console.print(f"[bold green]Iteration {i} in more like how we humans talk to each other. starting...[/bold green]")
        
        # # Wait for 10 seconds
        # console.print("[bold white]Waiting for 10 seconds...[/bold white]")
        # time.sleep(20)
        
        # # Right click
        # console.print("[bold white]Performing right click...[/bold white]")
        # pyautogui.click()
        
        # # Wait for 2 seconds
        # console.print("[bold white]Waiting for 2 seconds...[/bold white]")
        # time.sleep(2)
        
        # # Write "10 more like this"
        # console.print("[bold white]Writing '10 more like this'...[/bold white]")
        # pyautogui.write(f"{i} in more like how we humans talk to each other.. write 500 data sets. this in given format '{{''commond'': '',''emotion'': ''}} dont write in {{ \"command\": \"hi friday\", \"patterns\": [ \"Hello!\", \"Hi there!\", \"Hey!\", \"Good day!\", \"Greetings!\" ], \"responses\": [ \"Hello! How are you doing today?\", \"Good day! How are things with you?\", \"Greetings! How have you been?\" ]}} write as much asked. Note only 4 emotion sad,happy,excited,guilt")
        # pyautogui.press("enter")
        # # Wait for 122 seconds
        # console.print("[bold white]Waiting for 122 seconds...[/bold white]")
        
        time.sleep(90)
        # Right click again
        console.print("[bold white]Performing right click...[/bold white]")
        pyautogui.click()
        
        # Wait for 2 seconds
        console.print("[bold white]Waiting for 2 seconds...[/bold white]")
        time.sleep(2)
        
        # Write "10 more like this"
        console.print("[bold white]Writing '10 more like this' again...[/bold white]")
        pyautogui.write(f'{i} in more like how we humans talk to each other.')
        pyautogui.press("enter")
        # Wait for 122 seconds
        console.print("[bold white]Waiting for 122 seconds...[/bold white]")
        time.sleep(90)
        time.sleep(40)
        time.sleep(2)
        # Right click again
        console.print("[bold white]Performing right click...[/bold white]")
        pyautogui.click()
        
        # Wait for 2 seconds
        console.print("[bold white]Waiting for 2 seconds...[/bold white]")
        time.sleep(2)
        
        # Write "10 more like this"
        console.print("[bold white]Writing '10 more like this' again...[/bold white]")
        pyautogui.write(f'{i} in more like how we humans talk to each other.')
        pyautogui.press("enter")
        # Wait for 122 seconds
        console.print("[bold white]Waiting for 122 seconds...[/bold white]")
        time.sleep(90)
        time.sleep(40)
        time.sleep(2)
        # Right click again
        console.print("[bold white]Performing right click...[/bold white]")
        pyautogui.click()
        
        # Wait for 2 seconds
        console.print("[bold white]Waiting for 2 seconds...[/bold white]")
        time.sleep(2)
        
        # Write "10 more like this"
        console.print("[bold white]Writing '10 more like this' again...[/bold white]")
        pyautogui.write(f'{i} in more like how we humans talk to each other.')
        pyautogui.press("enter")
        # Wait for 122 seconds
        console.print("[bold white]Waiting for 122 seconds...[/bold white]")
        time.sleep(90)
        time.sleep(40)
        # Right click again
        console.print("[bold white]Performing right click...[/bold white]")
        pyautogui.click()
        
        # Wait for 2 seconds
        console.print("[bold white]Waiting for 2 seconds...[/bold white]")
        time.sleep(2)
        
        # Write "10 more like this"
        console.print("[bold white]Writing '10 more like this' again...[/bold white]")
        pyautogui.write(f'{i} in more like how we humans talk to each other.')
        pyautogui.press("enter")
        # Wait for 122 seconds
        console.print("[bold white]Waiting for 122 seconds...[/bold white]")
        time.sleep(90)
        time.sleep(40)
        # Right click again
        console.print("[bold white]Performing right click...[/bold white]")
        pyautogui.click()
        
        # Wait for 2 seconds
        console.print("[bold white]Waiting for 2 seconds...[/bold white]")
        time.sleep(2)
        
        # Write "10 more like this"
        console.print("[bold white]Writing '10 more like this' again...[/bold white]")
        pyautogui.write(f'{i} in more like how we humans talk to each other.')
        pyautogui.press("enter")
        # Wait for 122 seconds
        console.print("[bold white]Waiting for 122 seconds...[/bold white]")
        time.sleep(90)
        time.sleep(40)
    console.print("[bold green]Automation successful[/bold green]")

if __name__ == "__main__":
    automate_iui()
