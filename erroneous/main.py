import asyncio
import json
import aio_pika
from email_sendler import EmailNotificationService
from telegram_sendler import TelegramNotificationService



token = "6318131538:AAFVgE9nHLvQMMYMJWWRKcOzJ3PaPcPEIcw"
chanel = "-1001908502023"
password = "hjfk voxh yfck bwlw"
email_sender = "k1st.volkov@gmail.com"
smtp_server = "smtp.gmail.com"
email_port = 587
recipient = ["k1st.volkov@gmail.com"]

config_email = [email_sender, password, smtp_server, email_port, recipient]
config_telegram = [token, chanel]


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