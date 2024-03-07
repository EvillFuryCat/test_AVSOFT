import smtplib
from email.mime.text import MIMEText
from time import sleep


class EmailNotificationService:
    def __init__(self, sender: str, password: str, smtp_server: str, port: int, recipient: str) -> None:
        self.sender = sender
        self.password = password
        self.smtp_server = smtp_server
        self.port = port
        self.recipient = recipient
    
    def send_mail(self, message):
        server = smtplib.SMTP(self.smtp_server, self.port)
        server.starttls()
        
        try:
            server.login(self.sender, self.password)
            msg = MIMEText(message)
            server.sendmail(self.sender, self.recipient, f"Subject: ERROR n{msg}")
        except smtplib.SMTPException as e:
            print(f"Ошибка при отправке письма: {e}")
            print("Повторная попытка отправки через 60 секунд...")
            sleep(60)
            server.sendmail(self.sender, self.recipient, f"Subject: ERROR n{msg}")