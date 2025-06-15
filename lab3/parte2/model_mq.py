import pika
import json
def addUser(user):
    msg = {"type": "addUser", "data": user}
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='twitter-exchange', exchange_type='fanout', durable=False)
    channel.basic_publish(exchange='twitter-exchange', routing_key='', body=json.dumps(msg))
    connection.close()
def updateUser(token, user):
    msg = {"type": "updateUser", "token": token, "data": user}
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='twitter-exchange',exchange_type='fanout', durable=False)
    channel.basic_publish(exchange='twitter-exchange', routing_key='', body=json.dumps(msg))
    connection.close()
def removeUser(token): pass
def follow(token, nick): 
    msg = {"type": "follow", "token": token, "data": nick}
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='twitter-exchange',exchange_type='fanout', durable=False)
    channel.basic_publish(exchange='twitter-exchange', routing_key='', body=json.dumps(msg))
    connection.close()
def unfollow(token, user_id, nick): pass
def addTweet(token, content):
    msg = {"type": "addtweet", "token": token, "data": content}
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='twitter-exchange',exchange_type='fanout', durable=False)
    channel.basic_publish(exchange='twitter-exchange', routing_key='', body=json.dumps(msg))
    connection.close()
def retweet(token, tweet_id): pass
def like(token, tweet_id): pass
def dislike(token, tweet_id): pass
