import smtplib, ssl

import config

smtp_server = "smtp.mail.ru"
port = 587  # For starttls
sender_email = config.email
password = config.email_password

def send_email(errors):
    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender_email, password)
        # TODO: Send email here
        text = "\n".join(errors)
        email = f"""\
Subject: Error occured while parcing from https://www.adac.de/

{text}"""
        server.sendmail(sender_email, config.receiver_email, email)
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit()