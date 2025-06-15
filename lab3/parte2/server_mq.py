# server_mq.py
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

    try:
        if msg['type'] == 'addUser':
            print('add user')
            model.add_user(msg['data'])

        elif msg['type'] == 'updateUser':
            print('update user')
            model.update_user(msg['token'], msg['data'])

        elif msg['type'] == 'removeUser':
            print('remove user')
            model.remove_user(msg['token'])

        elif msg['type'] == 'follow':
            print('follow user')
            model.follow(msg['token'], msg['data'])

        elif msg['type'] == 'unfollow':
            print('unfollow user')
            model.unfollow(msg['token'], msg['data'])

        elif msg['type'] == 'addTweet':
            print('add tweet')
            model.add_tweet(msg['token'], msg['data'])

        elif msg['type'] == 'addRetweet':
            print('add retweet')
            model.add_retweet(msg['token'], msg['data'])

        elif msg['type'] == 'like':
            print('like tweet')
            model.like(msg['token'], msg['data'])

        elif msg['type'] == 'dislike':
            print('dislike tweet')
            model.dislike(msg['token'], msg['data'])

        else:
            print(f"Unknown message type: {msg['type']}")

    except Exception as exc:
        print(f"Error handling message: {exc}")

channel.basic_consume(queue='twitter-queue', on_message_callback=callback, auto_ack=True)
channel.start_consuming()
