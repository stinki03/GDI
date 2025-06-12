import pika
import json
import model_mongo as model

RABBIT_HOST = 'localhost'
EXCHANGE = 'twitter-exchange'
QUEUE = 'twitter-queue'

def callback(ch, method, properties, body):
    msg = json.loads(body)
    t = msg.get("type")
    try:
        if t == "addUser":
            model.addUser(msg["data"])
        elif t == "updateUser":
            model.updateUser(msg["token"], msg["id"], msg["data"])
        elif t == "removeUser":
            model.removeUser(msg["token"], msg["id"])
        elif t == "follow":
            model.follow(msg["token"], msg["id"], msg["nick"])
        elif t == "unfollow":
            model.unfollow(msg["token"], msg["id"], msg["nick"])
        elif t == "addTweet":
            model.addTweet(msg["token"], msg["data"]["content"])
        elif t == "addRetweet":
            model.addRetweet(msg["token"], msg["id"])
        elif t == "like":
            model.like(msg["token"], msg["id"])
        elif t == "dislike":
            model.dislike(msg["token"], msg["id"])
        else:
            print(f"Tipo de mensaje desconocido: {t}")
    except Exception as exc:
        print(f"Error procesando {t}: {exc}")

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_HOST))
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE, exchange_type='fanout', durable=False)
    channel.queue_declare(queue=QUEUE, durable=False)
    channel.queue_bind(exchange=EXCHANGE, queue=QUEUE, routing_key='')
    channel.basic_consume(queue=QUEUE, on_message_callback=callback, auto_ack=True)
    print("Esperando mensajes en RabbitMQ...")
    channel.start_consuming()

if __name__ == '__main__':
    main()
