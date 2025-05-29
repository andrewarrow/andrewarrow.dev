import os
import resend
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set Resend API key from environment variable
resend.api_key = os.getenv("RESEND")

def send_html_email():
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

    # Define email parameters
    params = {
        "from": "Showffeur App <showffeur@andrewarrow.dev>",
        "to": ["oneone@gmail.com"],
        "subject": "Thank you Beta Testers2",
        "html": html_content
    }

    try:
        # Send the email using Resend API
        response = resend.Emails.send(params)
        print("Email sent successfully:", response)
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    send_html_email()
