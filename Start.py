from instagrapi import Client
def send_insta(recipient_username, message):
    # Get username and password from user input
    username = "utkarsh_chaudhary_009"
    password ="utkarshchaudhary009"
    
    # Initialize the Instagram client
    client = Client()

    # Login to Instagram
    client.login(username, password)

    # Fetch recipient's user ID
    recipient_id = client.user_id_from_username(recipient_username)

    # Send a direct message
    client.direct_send(recipient_id, message)

    # Logout after sending the message (optional)
    client.logout()
