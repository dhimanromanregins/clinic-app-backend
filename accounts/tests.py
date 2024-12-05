import requests
import json

def send_expo_push_notification(message):
    """
    Send a push notification using Expo's Push Notification API.

    Args:
        message (dict): A dictionary containing the notification details.
                        Required fields:
                        - to: The Expo push token of the recipient.
                        - title: Title of the notification.
                        - body: Body content of the notification.

    Returns:
        dict or None: The JSON response if successful, or None if an error occurs.
    """
    url = "https://exp.host/--/api/v2/push/send"
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en",
        "Content-Type": "application/json",
    }
    try:
        # Send POST request to the Expo API
        response = requests.post(url, headers=headers, data=json.dumps(message))
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()  # Parse and return JSON response
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while sending notification: {e}")
        return None

if __name__ == "__main__":
    # Example message to send
    message = {
        "to": "ExponentPushToken[hHyNpaDvpxLJkpI4axXO3q]",  # Replace with the recipient's push token
        "title": "Hello from Expo!",
        "body": "This is a test notification.",
        "data": {"extra_info": "Optional data here"},  # Optional additional data
    }

    # Send notification
    response = send_expo_push_notification(message)

    # Check the response
    if response:
        print("Notification sent successfully!")
        print("Response:", json.dumps(response, indent=4))
    else:
        print("Failed to send notification.")
