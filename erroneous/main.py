import asyncio
import json
import aio_pika
from email_sendler import EmailNotificationService
from telegram_sendler import TelegramNotificationService


with open('config.json', 'r') as file:
    config_data = json.load(file)
    

token = config_data["token"]
channel = config_data["channel"]
password = config_data["password"]
email_sender = config_data["email_sender"]
smtp_server = config_data["smtp_server"]
email_port = config_data["email_port"]
recipient = config_data["recipient"]

config_email = [email_sender, password, smtp_server, email_port, recipient]
config_telegram = [token, channel]


class NotificationService(EmailNotificationService, TelegramNotificationService):
    def __init__(self, email_params, telegram_params):
        EmailNotificationService.__init__(self, *email_params)
        TelegramNotificationService.__init__(self, *telegram_params)
    
    async def consume_messages(self):
        connection = await aio_pika.connect_robust("amqp://guest:guest@rabbit/")
        channel = await connection.channel()
        queue = await channel.declare_queue('Errors', durable=True)

        async for message in queue:
            async with message.process():
                data = json.loads(message.body)
                await self.send_telegram_message_async(data['path'])
                self.send_mail(data['path'])

    async def main(self):
        await self.consume_messages()

if __name__ == '__main__':
    notification_service = NotificationService(config_email, config_telegram)
    asyncio.run(notification_service.main())