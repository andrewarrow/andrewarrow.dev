import os
import resend
from dotenv import load_dotenv
import argparse

# Load environment variables from .env file
load_dotenv()

# Set Resend API key from environment variable
resend.api_key = os.getenv("RESEND")

def send_html_email(to_address):
    # Read the HTML content from email.html
    try:
        with open("email.html", "r", encoding="utf-8") as file:
            html_content = file.read()
    except FileNotFoundError:
        print("Error: email.html file not found.")
        return
    except Exception as e:
        print(f"Error reading email.html: {e}")
        return

    # Add email to audience first
    audience_id = "516f95a7-9f86-4d08-ab50-4b1583ea7667"
    try:
        audience_response = resend.Audiences.add(
            audience_id=audience_id,
            email=to_address
        )
        print(f"Email added to audience: {audience_response}")
    except Exception as e:
        print(f"Failed to add email to audience: {e}")

    # Define email parameters
    params = {
        "from": "Showffeur App <showffeur@andrewarrow.dev>",
        "to": [to_address],
        "subject": "Thank you Beta Testers",
        "html": html_content
    }

    try:
        # Send the email using Resend API
        response = resend.Emails.send(params)
        print("Email sent successfully:", response)
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send an HTML email using Resend API")
    parser.add_argument(
        "--to",
        required=True,
        help="Recipient email address"
    )
    args = parser.parse_args()

    # Call the function with the provided to address
    send_html_email(args.to)
