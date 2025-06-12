# model_mongo.py
import pymongo
from bson import ObjectId
import time

def get_db():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    return client['twitter']

def require_login(func):
    def wrapper(token, *args, **kwargs):
        db = get_db()
        try:
            user = db.users.find_one({'_id': ObjectId(token)})
        except:
            user = None
        if not user:
            raise Exception("Invalid or expired token")
        return func(user, *args, **kwargs)
    return wrapper

def add_user(user):
    db = get_db()
    if not all(k in user for k in ("name","surname","email","password","nick")):
        raise Exception("Missing required fields")
    if db.users.find_one({"$or": [{"email": user['email']}, {'nick': user['nick']}] }):
        raise Exception("User already exists")
    user_doc = { **user, 'followers': [], 'following': [] }
    res = db.users.insert_one(user_doc)
    return str(res.inserted_id)

def login(email, password):
    db = get_db()
    user = db.users.find_one({"email": email, "password": password})
    if not user:
        raise Exception("Invalid email or password")
    return str(user['_id'])

@require_login
def list_users(current_user, query="", limit=20, skip=0):
    db = get_db()
    filt = {}
    if query:
        filt = {'$or': [
            {'name': {'$regex': query, '$options': 'i'}},
            {'surname': {'$regex': query, '$options': 'i'}},
            {'email': {'$regex': query, '$options': 'i'}},
            {'nick': {'$regex': query, '$options': 'i'}}
        ]}
    cursor = db.users.find(filt, {'password':0, 'followers':0, 'following':0}) \
                     .skip(skip).limit(limit)
    return [{k: str(v) for k,v in u.items() if k!='_id'} for u in cursor]

@require_login
def update_user(current_user, user):
    db = get_db()
    upd = {k: user[k] for k in ('name','surname','email','password','nick')}
    res = db.users.update_one({'_id': current_user['_id']}, {'$set': upd})
    return res.modified_count > 0

@require_login
def remove_user(current_user):
    db = get_db()
    uid = current_user['_id']
    # Borrar retweets huérfanos
    own_tweets = db.tweets.find({'user_id': uid}, {'_id':1})
    ids = [t['_id'] for t in own_tweets]
    db.tweets.delete_many({'ref_id': {'$in': ids}})
    # Borrar usuario y referencias
    db.users.delete_one({'_id': uid})
    db.users.update_many({}, {'$pull': {'followers': uid, 'following': uid}})
    # Borrar tweets originales
    db.tweets.delete_many({'user_id': uid})
    return True

@require_login
def follow(current_user, nick):
    db = get_db()
    target = db.users.find_one({'nick': nick})
    if not target:
        raise Exception("User not found")
    if target['_id'] == current_user['_id']:
        raise Exception("Cannot follow yourself")
    db.users.update_one({'_id': current_user['_id']}, {'$addToSet': {'following': target['_id']}})
    db.users.update_one({'_id': target['_id']}, {'$addToSet': {'followers': current_user['_id']}})
    return True

@require_login
def unfollow(current_user, nick):
    db = get_db()
    target = db.users.find_one({'nick': nick})
    if not target:
        raise Exception("User not found")
    db.users.update_one({'_id': current_user['_id']}, {'$pull': {'following': target['_id']}})
    db.users.update_one({'_id': target['_id']}, {'$pull': {'followers': current_user['_id']}})
    return True

@require_login
def list_following(current_user, query="", limit=20, skip=0):
    db = get_db()
    ids = current_user.get('following', [])
    filt = {'_id': {'$in': ids}}
    if query:
        filt['$or'] = [{'name': {'$regex': query, '$options': 'i'}}, {'nick': {'$regex': query, '$options': 'i'}}]
    cursor = db.users.find(filt, {'password':0,'followers':0,'following':0}) \
                     .skip(skip).limit(limit)
    return [{k: str(v) for k,v in u.items() if k!='_id'} for u in cursor]

@require_login
def list_followers(current_user, query="", limit=20, skip=0):
    db = get_db()
    ids = current_user.get('followers', [])
    filt = {'_id': {'$in': ids}}
    if query:
        filt['$or'] = [{'name': {'$regex': query, '$options': 'i'}}, {'nick': {'$regex': query, '$options': 'i'}}]
    cursor = db.users.find(filt, {'password':0,'followers':0,'following':0}) \
                     .skip(skip).limit(limit)
    return [{k: str(v) for k,v in u.items() if k!='_id'} for u in cursor]

@require_login
def add_tweet(current_user, content):
    db = get_db()
    now = int(time.time())
    doc = {
        'user_id': current_user['_id'],
        'content': content,
        'date': now,
        'ref_id': None,
        'likes': [],
        'dislikes': []
    }
    res = db.tweets.insert_one(doc)
    return {'id': str(res.inserted_id), 'content': content}

@require_login
def add_retweet(current_user, tweet_id):
    db = get_db()
    orig = db.tweets.find_one({'_id': ObjectId(tweet_id)})
    if not orig:
        raise Exception("Original tweet not found")
    now = int(time.time())
    doc = {
        'user_id': current_user['_id'],
        'content': '',
        'date': now,
        'ref_id': orig['_id'],
        'likes': [],
        'dislikes': []
    }
    res = db.tweets.insert_one(doc)
    return {'id': str(res.inserted_id), 'ref_id': tweet_id}

@require_login
def list_tweets(current_user, query="", limit=20, skip=0):
    db = get_db()
    feed_ids = current_user.get('following', []) + [current_user['_id']]
    filt = {'user_id': {'$in': feed_ids}}
    if query:
        filt['content'] = {'$regex': query, '$options': 'i'}
    cursor = db.tweets.find(filt).sort('date', -1).skip(skip).limit(limit)
    lst = []
    for t in cursor:
        user = db.users.find_one({'_id': t['user_id']})
        lst.append({
            'id': str(t['_id']),
            'content': t['content'],
            'date': t['date'],
            'ref_id': str(t['ref_id']) if t['ref_id'] else None,
            'nick': user['nick'],
            'likes': len(t.get('likes', [])),
            'dislikes': len(t.get('dislikes', []))
        })
    return lst

@require_login
def like(current_user, tweet_id):
    db = get_db()
    tid = ObjectId(tweet_id)
    db.tweets.update_one(
        {'_id': tid},
        {'$addToSet': {'likes': current_user['_id']}, '$pull': {'dislikes': current_user['_id']}}
    )
    return True

@require_login
def dislike(current_user, tweet_id):
    db = get_db()
    tid = ObjectId(tweet_id)
    db.tweets.update_one(
        {'_id': tid},
        {'$addToSet': {'dislikes': current_user['_id']}, '$pull': {'likes': current_user['_id']}}
    )
    return True

@require_login
def list_likes(current_user, tweet_id):
    db = get_db()
    t = db.tweets.find_one({'_id': ObjectId(tweet_id)})
    ids = t.get('likes', [])
    users = db.users.find({'_id': {'$in': ids}}, {'password':0,'followers':0,'following':0})
    return [{k: str(v) for k,v in u.items() if k!='_id'} for u in users]

@require_login
def list_dislikes(current_user, tweet_id):
    db = get_db()
    t = db.tweets.find_one({'_id': ObjectId(tweet_id)})
    ids = t.get('dislikes', [])
    users = db.users.find({'_id': {'$in': ids}}, {'password':0,'followers':0,'following':0})
    return [{k: str(v) for k,v in u.items() if k!='_id'} for u in users]
