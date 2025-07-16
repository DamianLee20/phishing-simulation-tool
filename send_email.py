import smtplib
from email.mime.text import MIMEText

def send_phishing_email(recipient_email):
    sender_email = "Dlee21221@gmail.com"
    sender_password = "tblvdbswimobzevs"

    with open("email_template.txt", "r") as f:
        body = f.read()

    msg = MIMEText(body)
    msg['Subject'] = "Urgent: Account Verification Required"
    msg['From'] = sender_email
    msg['To'] = recipient_email

    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, recipient_email, msg.as_string())
    server.quit()

if __name__ == "__main__":
    send_phishing_email("testuser@example.com")

