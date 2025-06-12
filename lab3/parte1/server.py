# server.py
import model_mongo as model
from flask import Flask, request

app = Flask(__name__)

@app.route('/twitter/sessions', methods=['POST'])
def login():
    creds = request.get_json()
    try:
        token = model.login(creds['email'], creds['password'])
        return {'token': token}
    except Exception as exc:
        return {'error': str(exc)}, 401

@app.route('/twitter/users', methods=['POST'])
def addUser():
    user = request.get_json()
    try:
        return model.addUser(user)
    except Exception as exc:
        return {'error': str(exc)}, 400

@app.route('/twitter/users', methods=['GET'])
def listUsers():
    token = request.args.get('token')
    query = request.args.get('filter', '')
    try:
        return model.listUsers(token, query)
    except Exception as exc:
        return {'error': str(exc)}, 400

@app.route('/twitter/users/<userId>', methods=['PUT'])
def updateUser(userId):
    token = request.args.get('token')
    user = request.get_json()
    try:
        updated = model.updateUser(token, userId, user)
        return {'updated': updated}
    except Exception as exc:
        return {'error': str(exc)}, 400

@app.route('/twitter/users/<userId>', methods=['DELETE'])
def removeUser(userId):
    token = request.args.get('token')
    try:
        deleted = model.removeUser(token, userId)
        return {'deleted': deleted}
    except Exception as exc:
        return {'error': str(exc)}, 400

@app.route('/twitter/users/<userId>/following', methods=['GET'])
def listFollowing(userId):
    token = request.args.get('token')
    query = request.args.get('filter', '')
    try:
        return model.listFollowing(token, userId, query)
    except Exception as exc:
        return {'error': str(exc)}, 400

@app.route('/twitter/users/<userId>/following', methods=['POST'])
def follow(userId):
    token = request.args.get('token')
    nick = request.get_json().get('nick')
    try:
        return {'followed': model.follow(token, userId, nick)}
    except Exception as exc:
        return {'error': str(exc)}, 400

@app.route('/twitter/users/<userId>/following/<nick>', methods=['DELETE'])
def unfollow(userId, nick):
    token = request.args.get('token')
    try:
        return {'unfollowed': model.unfollow(token, userId, nick)}
    except Exception as exc:
        return {'error': str(exc)}, 400

@app.route('/twitter/users/<userId>/followers', methods=['GET'])
def listFollowers(userId):
    token = request.args.get('token')
    query = request.args.get('filter', '')
    try:
        return model.listFollowers(token, userId, query)
    except Exception as exc:
        return {'error': str(exc)}, 400

@app.route('/twitter/tweets', methods=['POST'])
def addTweet():
    token = request.args.get('token')
    content = request.get_json().get('content')
    try:
        return model.addTweet(token, content)
    except Exception as exc:
        return {'error': str(exc)}, 400

@app.route('/twitter/tweets', methods=['GET'])
def listTweets():
    token = request.args.get('token')
    query = request.args.get('filter', '')
    try:
        return model.listTweets(token, query)
    except Exception as exc:
        return {'error': str(exc)}, 400

@app.route('/twitter/tweets/<tweetId>/retweets', methods=['POST'])
def retweet(tweetId):
    token = request.args.get('token')
    try:
        return model.addRetweet(token, tweetId)
    except Exception as exc:
        return {'error': str(exc)}, 400

@app.route('/twitter/tweets/<tweetId>/likes', methods=['POST'])
def like(tweetId):
    token = request.args.get('token')
    try:
        return {'liked': model.like(token, tweetId)}
    except Exception as exc:
        return {'error': str(exc)}, 400

@app.route('/twitter/tweets/<tweetId>/likes', methods=['GET'])
def listLikes(tweetId):
    token = request.args.get('token')
    try:
        return model.listLikes(token, tweetId)
    except Exception as exc:
        return {'error': str(exc)}, 400

@app.route('/twitter/tweets/<tweetId>/dislikes', methods=['POST'])
def dislike(tweetId):
    token = request.args.get('token')
    try:
        return {"success": model.dislike(token, tweetId)}
    except Exception as exc:
        return {'error': str(exc)}, 400

@app.route('/twitter/tweets/<tweetId>/dislikes', methods=['GET'])
def listDislikes(tweetId):
    token = request.args.get('token')
    try:
        return model.listDislikes(token, tweetId)
    except Exception as exc:
        return {'error': str(exc)}, 400
