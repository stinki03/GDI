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

@app.route('/twitter/users', methods=['GET'])
def listUsers():
    token = request.args.get('token')
    query = request.args.get('filter', '')
    try:
        return model.listUsers(token, query)
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

@app.route('/twitter/users/<userId>/followers', methods=['GET'])
def listFollowers(userId):
    token = request.args.get('token')
    query = request.args.get('filter', '')
    try:
        return model.listFollowers(token, userId, query)
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

@app.route('/twitter/tweets/<tweetId>/likes', methods=['GET'])
def listLikes(tweetId):
    token = request.args.get('token')
    try:
        return model.listLikes(token, tweetId)
    except Exception as exc:
        return {'error': str(exc)}, 400

@app.route('/twitter/tweets/<tweetId>/dislikes', methods=['GET'])
def listDislikes(tweetId):
    token = request.args.get('token')
    try:
        return model.listDislikes(token, tweetId)
    except Exception as exc:
        return {'error': str(exc)}, 400
