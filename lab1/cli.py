#!/usr/bin/python3
import model

def help():
    print("""
Available commands:
- help
- exit
- adduser <name> <surname> <email> <password> <nick>
- login <email> <password>
- listusers [<query>]
- updateuser <name> <surname> <email> <password> <nick>
- removeuser
- follow <nick>
- unfollow <nick>
- listfollowing [<query>]
- listfollowers [<query>]
- addtweet <content>
- addretweet <tweet_id>
- listtweets [<query>]
- like <tweet_id>
- dislike <tweet_id>
- listlikes <tweet_id>
- listdislikes <tweet_id>
""")

# Inicializar token como variable global
token = None

while True:
    cmd = input("> ").split(" ", 1)
    try:
        if cmd[0] == "help":
            help()
        elif cmd[0] == "exit":
            break
        elif cmd[0] == "adduser":
            if len(cmd) < 2:
                print("Usage: adduser <name> <surname> <email> <password> <nick>")
                continue
            args = cmd[1].split()
            if len(args) != 5:
                print("Usage: adduser <name> <surname> <email> <password> <nick>")
                continue
            user = {"name": args[0], "surname": args[1], "email": args[2], "password": args[3], "nick": args[4]}
            model.addUser(user)
            print("User added.")
        elif cmd[0] == "login":
            if len(cmd) < 2:
                print("Usage: login <email> <password>")
                continue
            args = cmd[1].split()
            if len(args) != 2:
                print("Usage: login <email> <password>")
                continue
            token = model.login(args[0], args[1])
            print("Welcome!")
        elif not token:
            print("Please login first.")
        elif cmd[0] == "listusers":
            query = cmd[1] if len(cmd) > 1 else ""
            users = model.listUsers(token, query)
            for user in users:
                print(f"- {user}")
        elif cmd[0] == "updateuser":
            if len(cmd) < 2:
                print("Usage: updateuser <name> <surname> <email> <password> <nick>")
                continue
            args = cmd[1].split()
            if len(args) != 5:
                print("Usage: updateuser <name> <surname> <email> <password> <nick>")
                continue
            user = {"name": args[0], "surname": args[1], "email": args[2], "password": args[3], "nick": args[4]}
            updated = model.updateUser(token, user)
            print(f"User updated: {updated}")
        elif cmd[0] == "removeuser":
            model.removeUser(token)
            token = None
            print("User removed.")
        elif cmd[0] == "follow":
            if len(cmd) < 2:
                print("Usage: follow <nick>")
                continue
            model.follow(token, cmd[1])
            print("Followed.")
        elif cmd[0] == "unfollow":
            if len(cmd) < 2:
                print("Usage: unfollow <nick>")
                continue
            model.unfollow(token, cmd[1])
            print("Unfollowed.")
        elif cmd[0] == "listfollowing":
            query = cmd[1] if len(cmd) > 1 else ""
            users = model.listFollowing(token, query)
            for user in users:
                print(f"- {user}")
        elif cmd[0] == "listfollowers":
            query = cmd[1] if len(cmd) > 1 else ""
            users = model.listFollowers(token, query)
            for user in users:
                print(f"- {user}")
        elif cmd[0] == "addtweet":
            if len(cmd) < 2:
                print("Usage: addtweet <content>")
                continue
            tweet = model.addTweet(token, cmd[1])
            print(f"Tweet added: {tweet}")
        elif cmd[0] == "addretweet":
            if len(cmd) < 2:
                print("Usage: addretweet <tweet_id>")
                continue
            retweet = model.addRetweet(token, cmd[1])
            print(f"Retweet added: {retweet}")
        elif cmd[0] == "listtweets":
            query = cmd[1] if len(cmd) > 1 else ""
            tweets = model.listTweets(token, query)
            for tweet in tweets:
                print(f"- {tweet}")
        elif cmd[0] == "like":
            if len(cmd) < 2:
                print("Usage: like <tweet_id>")
                continue
            model.like(token, cmd[1])
            print("Liked.")
        elif cmd[0] == "dislike":
            if len(cmd) < 2:
                print("Usage: dislike <tweet_id>")
                continue
            model.dislike(token, cmd[1])
            print("Disliked.")
        elif cmd[0] == "listlikes":
            if len(cmd) < 2:
                print("Usage: listlikes <tweet_id>")
                continue
            users = model.listLikes(token, cmd[1])
            for user in users:
                print(f"- {user}")
        elif cmd[0] == "listdislikes":
            if len(cmd) < 2:
                print("Usage: listdislikes <tweet_id>")
                continue
            users = model.listDislikes(token, cmd[1])
            for user in users:
                print(f"- {user}")
        else:
            help()
    except Exception as e:
        print(f"Error: {e}")