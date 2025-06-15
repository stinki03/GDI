# cli.py
#!/usr/bin/python3
import model_mongo as model

def help():
    print("""
Available commands:
- help
- exit
- adduser <name> <surname> <email> <password> <nick>
- login <email> <password>
- listusers [<query>] [<limit>] [<skip>]
- updateuser <name> <surname> <email> <password> <nick>
- removeuser
- follow <nick>
- unfollow <nick>
- listfollowing [<query>] [<limit>] [<skip>]
- listfollowers [<query>] [<limit>] [<skip>]
- addtweet <content>
- addretweet <tweet_id>
- listtweets [<query>] [<limit>] [<skip>]
- like <tweet_id>
- dislike <tweet_id>
- listlikes <tweet_id>
- listdislikes <tweet_id>
""")

token = None

while True:
    cmd = input("> ").split()
    if not cmd:
        continue
    cmd_name = cmd[0]
    args = cmd[1:]
    try:
        if cmd_name == "help":
            help()
        elif cmd_name == "exit":
            break
        elif cmd_name == "adduser":
            if len(args) != 5:
                print("Usage: adduser <name> <surname> <email> <password> <nick>")
                continue
            user = {
                "name": args[0],
                "surname": args[1],
                "email": args[2],
                "password": args[3],
                "nick": args[4]
            }
            model.add_user(user)
            print("User added.")
        elif cmd_name == "login":
            if len(args) != 2:
                print("Usage: login <email> <password>")
                continue
            token = model.login(args[0], args[1])
            print("Welcome! Your session token is set.")
        elif not token:
            print("Please login first.")
        elif cmd_name == "listusers":
            query = args[0] if len(args) > 0 else ""
            limit = int(args[1]) if len(args) > 1 else 20
            skip  = int(args[2]) if len(args) > 2 else 0
            users = model.list_users(token, query=query, limit=limit, skip=skip)
            print(f"Found {len(users)} users:")
            for u in users:
                print("-", u)
        elif cmd_name == "updateuser":
            if len(args) != 5:
                print("Usage: updateuser <name> <surname> <email> <password> <nick>")
                continue
            user = {
                "name": args[0],
                "surname": args[1],
                "email": args[2],
                "password": args[3],
                "nick": args[4]
            }
            ok = model.update_user(token, user)
            print("User updated." if ok else "No changes made.")
        elif cmd_name == "removeuser":
            model.remove_user(token)
            token = None
            print("User removed.")
        elif cmd_name == "follow":
            if len(args) != 1:
                print("Usage: follow <nick>")
                continue
            model.follow(token, args[0])
            print("Followed.")
        elif cmd_name == "unfollow":
            if len(args) != 1:
                print("Usage: unfollow <nick>")
                continue
            model.unfollow(token, args[0])
            print("Unfollowed.")
        elif cmd_name == "listfollowing":
            query = args[0] if len(args) > 0 else ""
            limit = int(args[1]) if len(args) > 1 else 20
            skip  = int(args[2]) if len(args) > 2 else 0
            lst = model.list_following(token, query=query, limit=limit, skip=skip)
            for u in lst:
                print("-", u)
        elif cmd_name == "listfollowers":
            query = args[0] if len(args) > 0 else ""
            limit = int(args[1]) if len(args) > 1 else 20
            skip  = int(args[2]) if len(args) > 2 else 0
            lst = model.list_followers(token, query=query, limit=limit, skip=skip)
            for u in lst:
                print("-", u)
        elif cmd_name == "addtweet":
            if len(args) < 1:
                print("Usage: addtweet <content>")
                continue
            content = " ".join(args)
            tw = model.add_tweet(token, content)
            print("Tweet added:", tw)
        elif cmd_name == "addretweet":
            if len(args) != 1:
                print("Usage: addretweet <tweet_id>")
                continue
            rt = model.add_retweet(token, args[0])
            print("Retweet added:", rt)
        elif cmd_name == "listtweets":
            query = args[0] if len(args) > 0 else ""
            limit = int(args[1]) if len(args) > 1 else 20
            skip  = int(args[2]) if len(args) > 2 else 0
            lst = model.list_tweets(token, query=query, limit=limit, skip=skip)
            for t in lst:
                print(f"- [{t['nick']}] {t['content']} (id={t['id']})")
        elif cmd_name == "like":
            if len(args) != 1:
                print("Usage: like <tweet_id>")
                continue
            model.like(token, args[0])
            print("Liked.")
        elif cmd_name == "dislike":
            if len(args) != 1:
                print("Usage: dislike <tweet_id>")
                continue
            model.dislike(token, args[0])
            print("Disliked.")
        elif cmd_name == "listlikes":
            if len(args) != 1:
                print("Usage: listlikes <tweet_id>")
                continue
            lst = model.list_likes(token, args[0])
            for u in lst:
                print("-", u)
        elif cmd_name == "listdislikes":
            if len(args) != 1:
                print("Usage: listdislikes <tweet_id>")
                continue
            lst = model.list_dislikes(token, args[0])
            for u in lst:
                print("-", u)
        else:
            help()
    except Exception as e:
        print(f"Error: {e}")
