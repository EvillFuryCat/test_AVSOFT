import pika


class RabbitManager:
    def __init__(
        self,
        host: str = "rabbit",
        port: int =5672,
        login: str = "guest",
        password: str = "guest"
        ):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=host,
            port=port,
            credentials=pika.PlainCredentials(
                username=login,
                password=password
                )
            )
                                                  )
        self.channel = self.connection.channel()
        
        
    def create_queue(self, queue_name: str) -> None:
        self.channel.queue_declare(queue=queue_name, durable=True)
        
    
    def send_message(self, message: str, queue_name: str) -> None:
        self.channel.basic_publish(exchange='', routing_key=queue_name, body=message)
    
    def consume_messages(self, queue_name, callback):
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

