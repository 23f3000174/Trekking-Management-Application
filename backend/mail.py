import smtplib
from email.mime.text import MIMEText

SMTP_HOST = 'localhost'
SMTP_PORT = 1025
FROM_EMAIL = 'admin@admin.com'

def send_mail(to_email, subject, body):
    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.sendmail(FROM_EMAIL, [to_email], msg.as_string())

if __name__ == "__main__":
    from app import create_app
    from models.models import User

    app = create_app()
    with app.app_context():

        admin_user = User.query.first()
        if admin_user:
            print(f"Testing mail sending to first user: {admin_user.email}")
            try:
                send_mail(admin_user.email, "Test Subject", "<h3>Hello Test</h3>")
                print("Mail sent successfully!")
            except Exception as e:
                print(f"Failed to send mail: {e}")
        else:
            print("No users found to test mail sending.")