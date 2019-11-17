import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

message = Mail(
    from_email="from_email@example.com",
    to_emails="tomhill98@me.com",
    subject="Sending with Twilio SendGrid is Fun",
    html_content="<strong>and easy to do anywhere, even with Python</strong>",
)


def send_message():
    try:
        sg = SendGridAPIClient(os.environ.get("SENDGRID_KEY"))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))