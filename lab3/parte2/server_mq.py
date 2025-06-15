import pika
import json
import model_mongo as model

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='twitter-exchange', exchange_type='fanout', durable=False)
channel.queue_declare(queue='twitter-queue', durable=False)
channel.queue_bind(exchange='twitter-exchange', queue='twitter-queue', routing_key='')

def callback(ch, method, properties, body):
    print(f"Received: {body}")
    msg = json.loads(body)
    if msg['type'] == 'addUser':
        print('add user')
        try:
            model.addUser(msg['data'])
        except Exception as exc:
            print(exc)
    elif msg['type'] == 'updateUser':
        print('update user')
        try:
            model.updateUser(msg['token', msg['data']])
        except Exception as exc:
            print(exc)
    elif msg['type'] == 'removeUser': pass
    elif msg['type'] == 'follow': pass
    elif msg['type'] == 'unfollow': pass
    elif msg['type'] == 'addTweet': pass
    elif msg['type'] == 'addRetweet': pass
    elif msg['type'] == 'like': pass
    elif msg['type'] == 'dislike': pass
    else: pass
channel.basic_consume(queue='twitter-queue', on_message_callback=callback, auto_ack=True)
channel.start_consuming()

