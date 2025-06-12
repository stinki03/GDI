# cli.py
# -*- coding: utf-8 -*-
import model_mq as mq
import model_rest as rest

token = None
user_id = None

def login():
    global token, user_id
    print("\n--- Iniciar sesion ---")
    email = input("Email: ")
    password = input("Password: ")
    try:
        token = rest.login(email, password)
        user_id = token
        print("Sesion iniciada correctamente.")
    except Exception as e:
        print("Error:", e)

def register():
    print("\n--- Registrar usuario (async) ---")
    user = {
        "name": input("Nombre: "),
        "surname": input("Apellido: "),
        "email": input("Email: "),
        "password": input("Password: "),
        "nick": input("Nick: ")
    }
    mq.addUser(user)
    print("Solicitud de creacion encolada.")

def list_users():
    print("\n--- Lista de usuarios ---")
    try:
        users = rest.listUsers(token)
        for u in users:
            print(f"{u['nick']} - {u['email']}")
    except Exception as e:
        print("Error:", e)

def update_user():
    print("\n--- Actualizar usuario (async) ---")
    user = {
        "name": input("Nuevo nombre: "),
        "surname": input("Nuevo apellido: "),
        "email": input("Nuevo email: "),
        "password": input("Nueva password: "),
        "nick": input("Nuevo nick: ")
    }
    mq.updateUser(token, user_id, user)
    print("Solicitud de actualizacion encolada.")

def remove_user():
    print("\n--- Eliminar usuario (async) ---")
    if input("Seguro? (s/n): ").lower() != "s":
        return
    mq.removeUser(token, user_id)
    print("Solicitud de eliminacion encolada.")

def follow_user():
    print("\n--- Seguir usuario (async) ---")
    nick = input("Nick a seguir: ")
    mq.follow(token, user_id, nick)
    print("Solicitud de follow encolada.")

def unfollow_user():
    print("\n--- Dejar de seguir (async) ---")
    nick = input("Nick a dejar de seguir: ")
    mq.unfollow(token, user_id, nick)
    print("Solicitud de unfollow encolada.")

def list_following():
    print("\n--- Siguiendo ---")
    try:
        users = rest.listFollowing(token, user_id)
        for u in users:
            print(u["nick"])
    except Exception as e:
        print("Error:", e)

def list_followers():
    print("\n--- Seguidores ---")
    try:
        users = rest.listFollowers(token, user_id, "")
        for u in users:
            print(u["nick"])
    except Exception as e:
        print("Error:", e)

def post_tweet():
    print("\n--- Publicar tweet (async) ---")
    content = input("Contenido tweet: ")
    mq.addTweet(token, content)
    print("Tweet encolado.")

def retweet():
    print("\n--- Retuitear (async) ---")
    tid = input("ID tweet a retuitear: ")
    mq.addRetweet(token, tid)
    print("Retweet encolado.")

def list_tweets():
    print("\n--- Tweets ---")
    try:
        tweets = rest.listTweets(token)
        for t in tweets:
            ref = f"(retweet de {t['ref_id']})" if t.get("ref_id") else ""
            print(f"[{t['nick']}] {t['content']} {ref} (ID: {t['id']})")
    except Exception as e:
        print("Error:", e)

def like_tweet():
    print("\n--- Like tweet (async) ---")
    tid = input("ID tweet a likear: ")
    mq.like(token, tid)
    print("Like encolado.")

def dislike_tweet():
    print("\n--- Dislike tweet (async) ---")
    tid = input("ID tweet a dislikear: ")
    mq.dislike(token, tid)
    print("Dislike encolado.")

def list_likes():
    print("\n--- Likes de un tweet ---")
    tid = input("ID tweet para ver likes: ")
    try:
        users = rest.listLikes(token, tid)
        for u in users:
            print(u["nick"])
    except Exception as e:
        print("Error:", e)

def list_dislikes():
    print("\n--- Dislikes de un tweet ---")
    tid = input("ID tweet para ver dislikes: ")
    try:
        users = rest.listDislikes(token, tid)
        for u in users:
            print(u["nick"])
    except Exception as e:
        print("Error:", e)

def show_menu():
    print("""
==== Twitter Lite CLI ====
1. adduser
2. login
3. listusers
4. updateuser
5. removeuser
6. follow
7. unfollow
8. listfollowing
9. listfollowers
10. addtweet
11. addRetweet
12. listtweets
13. like
14. dislike
15. listlikes
16. listdislikes
0. exit
""")

def main():
    while True:
        show_menu()
        choice = input("Opcion: ").strip()
        if choice == "0":
            print("Hasta luego.")
            break
        ops = {
            "1": register, "2": login, "3": list_users,
            "4": update_user, "5": remove_user,
            "6": follow_user, "7": unfollow_user,
            "8": list_following, "9": list_followers,
            "10": post_tweet, "11": retweet,
            "12": list_tweets, "13": like_tweet,
            "14": dislike_tweet, "15": list_likes,
            "16": list_dislikes
        }
        action = ops.get(choice)
        if action:
            if choice not in ("1", "2") and token is None:
                print("Inicia sesion primero.")
            else:
                action()
        else:
            print("Opcion no valida.")

if __name__ == "__main__":
    main()