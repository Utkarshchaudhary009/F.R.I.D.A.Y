import webbrowser
import subprocess
import shutil

def open_website(arguments):
    url = arguments.get("url")

    if not url:
        return {"response": "Please specify a URL to open."}

    # Normalize URL
    if not url.startswith("http"):
        if "." not in url:
            url += ".com"  # Default to .com if no domain is provided
        url = "http://" + url

    chrome_path = shutil.which("chrome") or shutil.which("google-chrome")
    if chrome_path:
        subprocess.run([chrome_path, url])
        return {"response": f"Opening {url} in Chrome."}
    else:
        webbrowser.open(url)
        return {"response": f"Opening {url} in the default browser."}
