import pika
import json

RABBIT_HOST = 'localhost'
EXCHANGE = 'twitter-exchange'

def _publish(msg: dict):
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_HOST))
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE, exchange_type='fanout', durable=False)
    channel.basic_publish(exchange=EXCHANGE, routing_key='', body=json.dumps(msg))
    connection.close()

def addUser(user):
    _publish({"type": "addUser", "data": user})

def updateUser(token, user_id, user):
    _publish({"type": "updateUser", "token": token, "id": user_id, "data": user})

def removeUser(token, user_id):
    _publish({"type": "removeUser", "token": token, "id": user_id})

def follow(token, user_id, nick):
    _publish({"type": "follow", "token": token, "id": user_id, "nick": nick})

def unfollow(token, user_id, nick):
    _publish({"type": "unfollow", "token": token, "id": user_id, "nick": nick})

def addTweet(token, content):
    _publish({"type": "addTweet", "token": token, "data": {"content": content}})

def addRetweet(token, tweet_id):
    _publish({"type": "addRetweet", "token": token, "id": tweet_id})

def like(token, tweet_id):
    _publish({"type": "like", "token": token, "id": tweet_id})

def dislike(token, tweet_id):
    _publish({"type": "dislike", "token": token, "id": tweet_id})
