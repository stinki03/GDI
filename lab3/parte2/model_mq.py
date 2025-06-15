# model_mq.py
import pika
import json

def addUser(user):
    msg = {"type": "addUser", "data": user}
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='twitter-exchange', exchange_type='fanout', durable=False)
    channel.basic_publish(exchange='twitter-exchange', routing_key='', body=json.dumps(msg))
    connection.close()
    return user

def updateUser(token, user):
    msg = {"type": "updateUser", "token": token, "data": user}
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='twitter-exchange',exchange_type='fanout', durable=False)
    channel.basic_publish(exchange='twitter-exchange', routing_key='', body=json.dumps(msg))
    connection.close()

def removeUser(token):
    msg = {"type": "removeUser", "token": token}
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='twitter-exchange', exchange_type='fanout', durable=False)
    channel.basic_publish(exchange='twitter-exchange', routing_key='', body=json.dumps(msg))
    connection.close()

def follow(token, nick): 
    msg = {"type": "follow", "token": token, "data": nick}
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='twitter-exchange',exchange_type='fanout', durable=False)
    channel.basic_publish(exchange='twitter-exchange', routing_key='', body=json.dumps(msg))
    connection.close()

def unfollow(token, nick):
    msg = {"type": "unfollow", "token": token, "data": nick}
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='twitter-exchange', exchange_type='fanout', durable=False)
    channel.basic_publish(exchange='twitter-exchange', routing_key='', body=json.dumps(msg))
    connection.close()

def addTweet(token, content):
    msg = {"type": "addTweet", "token": token, "data": content}
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='twitter-exchange',exchange_type='fanout', durable=False)
    channel.basic_publish(exchange='twitter-exchange', routing_key='', body=json.dumps(msg))
    connection.close()

def addRetweet(token, tweet_id):
    msg = {"type": "addRetweet", "token": token, "data": tweet_id}
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='twitter-exchange', exchange_type='fanout', durable=False)
    channel.basic_publish(exchange='twitter-exchange', routing_key='', body=json.dumps(msg))
    connection.close()

def like(token, tweet_id):
    msg = {"type": "like", "token": token, "data": tweet_id}
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='twitter-exchange', exchange_type='fanout', durable=False)
    channel.basic_publish(exchange='twitter-exchange', routing_key='', body=json.dumps(msg))
    connection.close()

def dislike(token, tweet_id):
    msg = {"type": "dislike", "token": token, "data": tweet_id}
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='twitter-exchange', exchange_type='fanout', durable=False)
    channel.basic_publish(exchange='twitter-exchange', routing_key='', body=json.dumps(msg))
    connection.close()
