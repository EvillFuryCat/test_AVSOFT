import asyncio
import telegram



class TelegramNotificationService:
    def __init__(self, token: str, channel: str) -> None:
        self.token = token
        self.channel = channel
    
    async def send_telegram_message_async(self, message):
        bot = telegram.Bot(token=self.token)
        try:
            await bot.send_message(chat_id=self.channel, text=message)
        except telegram.error.RetryAfter as e:
            await asyncio.sleep(e.retry_after)
            await self.send_telegram_message_async(message)