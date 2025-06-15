# cli.py
import model_rest as model
import model_mq as mq

token = None
user_id = None

def login():
    global token, user_id
    print("\n--- Iniciar sesión ---")
    email = input("Email: ")
    password = input("Password: ")
    try:
        token = model.login(email, password)
        user_id = token  # para simplificar, token y userId son lo mismo
        print("Sesión iniciada correctamente.")
    except Exception as e:
        print("Error:", e)

def register():
    print("\n--- Registrar usuario ---")
    user = {
        "name": input("Nombre: "),
        "surname": input("Apellido: "),
        "email": input("Email: "),
        "password": input("Password: "),
        "nick": input("Nick: ")
    }
    try:
        mq.addUser(user)
        print("Usuario enviado al servidor MQ.")
    except Exception as e:
        print("Error:", e)

def update_user():
    print("\n--- Actualizar usuario ---")
    user = {
        "name": input("Nuevo nombre: "),
        "surname": input("Nuevo apellido: "),
        "email": input("Nuevo email: "),
        "password": input("Nueva password: "),
        "nick": input("Nuevo nick: ")
    }
    try:
        mq.updateUser(token, user)
        print("Actualización enviada al servidor MQ.")
    except Exception as e:
        print("Error:", e)

def remove_user():
    print("\n--- Eliminar usuario ---")
    confirm = input("¿Seguro? (s/n): ")
    if confirm.lower() != "s":
        return
    try:
        mq.removeUser(token, user_id)
        print("Eliminación enviada al servidor MQ.")
    except Exception as e:
        print("Error:", e)

def follow_user():
    followed = input("ID del usuario a seguir: ")
    try:
        mq.follow(token, followed)
        print("Petición de seguir enviada.")
    except Exception as e:
        print("Error:", e)

def unfollow_user():
    followed = input("ID del usuario a dejar de seguir: ")
    try:
        mq.unfollow(token, followed)
        print("Petición de dejar de seguir enviada.")
    except Exception as e:
        print("Error:", e)

def post_tweet():
    content = input("Contenido tweet: ")
    try:
        mq.addTweet(token, content)
        print("Tweet enviado.")
    except Exception as e:
        print("Error:", e)

def retweet():
    tweet_id = input("ID tweet a retuitear: ")
    try:
        mq.addRetweet(token, tweet_id)
        print("Retweet enviado.")
    except Exception as e:
        print("Error:", e)

def like_tweet():
    tweet_id = input("ID del tweet a likear: ")
    try:
        mq.like(token, tweet_id)
        print("Like enviado.")
    except Exception as e:
        print("Error:", e)

def dislike_tweet():
    tweet_id = input("ID del tweet a dislikear: ")
    try:
        mq.dislike(token, tweet_id)
        print("Dislike enviado.")
    except Exception as e:
        print("Error:", e)

def list_users():
    try:
        print("\n--- Lista de usuarios ---")
        users = model.listUsers(token)
        for u in users:
            print(f"{u['nick']} - {u['email']}")
    except Exception as e:
        print("Error:", e)

def list_following():
    try:
        print("\n--- Siguiendo ---")
        users = model.listFollowing(token, user_id)
        for u in users:
            print(u["nick"])
    except Exception as e:
        print("Error:", e)

def list_followers():
    try:
        print("\n--- Seguidores ---")
        users = model.listFollowers(token, user_id)
        for u in users:
            print(u["nick"])
    except Exception as e:
        print("Error:", e)

def list_tweets():
    try:
        print("\n--- Tweets ---")
        tweets = model.listTweets(token)
        for t in tweets:
            ref = f"(retweet de {t['ref_id']})" if t.get("ref_id") else ""
            print(f"[{t['nick']}] {t['content']} {ref} (ID: {t['id']})")
    except Exception as e:
        print("Error:", e)

def list_likes():
    tweet_id = input("ID del tweet para ver likes: ")
    try:
        users = model.listLikes(token, tweet_id)
        for u in users:
            print(u["nick"])
    except Exception as e:
        print("Error:", e)

def list_dislikes():
    tweet_id = input("ID del tweet para ver dislikes: ")
    try:
        users = model.listDislikes(token, tweet_id)
        for u in users:
            print(u["nick"])
    except Exception as e:
        print("Error:", e)

def show_menu():
    print("""
==== Twitter Lite CLI ====
1. adduser
2. login
3. updateuser
4. removeuser
5. follow
6. unfollow
7. addtweet
8. addRetweet
9. like
10. dislike
11. listusers
12. listfollowing
13. listfollowers
14. listtweets
15. listlikes
16. listdislikes
0. exit
""")

def main():
    while True:
        show_menu()
        choice = input("Opción: ").strip()
        ops = {
            "1": register, "2": login, "3": update_user,
            "4": remove_user, "5": follow_user, "6": unfollow_user,
            "7": post_tweet, "8": retweet, "9": like_tweet,
            "10": dislike_tweet, "11": list_users, "12": list_following,
            "13": list_followers, "14": list_tweets,
            "15": list_likes, "16": list_dislikes
        }
        if choice == "0":
            print("Hasta luego.")
            break
        action = ops.get(choice)
        if action:
            if choice not in ("1", "2") and token is None:
                print("Inicia sesión primero.")
            else:
                action()
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
