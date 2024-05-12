import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email configuration
sender_email = "shreyajprakash24@gmail.com"
password = "dxzehptaecftdbnw"

def mailsend(receiver_email, subject, body):
    try:
        # Create message object instance
        message = MIMEMultipart()

        # Email subject and body
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject

        # Add body to email
        body = body
        message.attach(MIMEText(body, "plain"))

        # Connect to the SMTP server
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, password)
            text = message.as_string()
            server.sendmail(sender_email, receiver_email, text)
            print("Email sent successfully!")
    except Exception as e:
        print("An error occurred while sending the email:", str(e))

# Example usage
'''try:
    mailsend("recipient@example.com", "Test Subject", "Test Body")
except Exception as e:
    print("An error occurred:", str(e))'''
