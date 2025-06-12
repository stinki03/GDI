# model_rest.py
import requests

base = "http://localhost:5000/twitter"

def login(email, password):
    resp = requests.post(f"{base}/sessions", json={"email": email, "password": password})
    if resp.ok:
        return resp.json()["token"]
    raise Exception(resp.text)

def addUser(user):
    resp = requests.post(f"{base}/users", json=user)
    if resp.ok:
        return resp.json()
    raise Exception(resp.text)

def listUsers(token, query=""):
    resp = requests.get(f"{base}/users", params={"token": token, "filter": query})
    if resp.ok:
        return resp.json()
    raise Exception(resp.text)

def updateUser(token, userId, user):
    resp = requests.put(f"{base}/users/{userId}", params={"token": token}, json=user)
    if resp.ok:
        return resp.json()
    raise Exception(resp.text)

def removeUser(token, userId):
    resp = requests.delete(f"{base}/users/{userId}", params={"token": token})
    if resp.ok:
        return resp.json()
    raise Exception(resp.text)

def listFollowing(token, userId, query):
    resp = requests.get(f"{base}/users/{userId}/following", params={"token": token, "filter": query})
    if resp.ok:
        return resp.json()
    raise Exception(resp.text)

def follow(token, userId, nick):
    resp = requests.post(f"{base}/users/{userId}/following", params={"token": token}, json={"nick": nick})
    if resp.ok:
        return resp.json()
    raise Exception(resp.text)

def unfollow(token, userId, nick):
    resp = requests.delete(f"{base}/users/{userId}/following/{nick}", params={"token": token})
    if resp.ok:
        return resp.json()
    raise Exception(resp.text)

def listFollowers(token, userId, query=""):
    resp = requests.get(f"{base}/users/{userId}/followers", params={"token": token, "filter": query})
    if resp.ok:
        return resp.json()
    raise Exception(resp.text)

def addTweet(token, content):
    resp = requests.post(f"{base}/tweets", params={"token": token}, json={"content": content})
    if resp.ok:
        return resp.json()
    raise Exception(resp.text)

def listTweets(token, query=""):
    resp = requests.get(f"{base}/tweets", params={"token": token, "filter": query})
    if resp.ok:
        return resp.json()
    raise Exception(resp.text)

def retweet(token, tweetId):
    resp = requests.post(f"{base}/tweets/{tweetId}/retweets", params={"token": token})
    if resp.ok:
        return resp.json()
    raise Exception(resp.text)

def like(token, tweetId):
    resp = requests.post(f"{base}/tweets/{tweetId}/likes", params={"token": token})
    if resp.ok:
        return resp.json()
    raise Exception(resp.text)

def listLikes(token, tweetId):
    resp = requests.get(f"{base}/tweets/{tweetId}/likes", params={"token": token})
    if resp.ok:
        return resp.json()
    raise Exception(resp.text)

def dislike(token, tweetId):
    resp = requests.post(f"{base}/tweets/{tweetId}/dislikes", params={"token": token})
    if resp.ok:
        return resp.json()
    raise Exception(resp.text)

def listDislikes(token, tweetId):
    resp = requests.get(f"{base}/tweets/{tweetId}/dislikes", params={"token": token})
    if resp.ok:
        return resp.json()
    raise Exception(resp.text)
