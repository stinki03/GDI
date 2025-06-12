# cli.py
import model_rest as model

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
        response = model.addUser(user)
        print("Usuario creado:", response["nick"])
    except Exception as e:
        print("Error:", e)

def list_users():
    print("\n--- Lista de usuarios ---")
    try:
        users = model.listUsers(token)
        for u in users:
            print(f"{u['nick']} - {u['email']}")
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
        res = model.updateUser(token, user_id, user)
        print("Usuario actualizado:", res)
    except Exception as e:
        print("Error:", e)

def remove_user():
    print("\n--- Eliminar usuario ---")
    confirm = input("¿Seguro? (s/n): ")
    if confirm.lower() != "s":
        return
    try:
        res = model.removeUser(token, user_id)
        print("Usuario eliminado:", res)
    except Exception as e:
        print("Error:", e)

def follow_user():
    nick = input("Nick del usuario a seguir: ")
    try:
        res = model.follow(token, user_id, nick)
        print("Siguiendo:", res)
    except Exception as e:
        print("Error:", e)

def unfollow_user():
    nick = input("Nick del usuario a dejar de seguir: ")
    try:
        res = model.unfollow(token, user_id, nick)
        print("Dejaste de seguir:", res)
    except Exception as e:
        print("Error:", e)

def list_following():
    print("\n--- Siguiendo ---")
    try:
        users = model.listFollowing(token, user_id)
        for u in users:
            print(u["nick"])
    except Exception as e:
        print("Error:", e)

def list_followers():
    print("\n--- Seguidores ---")
    try:
        users = model.listFollowers(token, user_id)
        for u in users:
            print(u["nick"])
    except Exception as e:
        print("Error:", e)

def post_tweet():
    content = input("Contenido tweet: ")
    try:
        t = model.addTweet(token, content)
        print("Tweet publicado:", t["id"])
    except Exception as e:
        print("Error:", e)

def retweet():
    tweet_id = input("ID tweet a retuitear: ")
    try:
        rt = model.retweet(token, tweet_id)
        print("Retweet publicado:", rt.get("id"))
    except Exception as e:
        print("Error:", e)

def list_tweets():
    print("\n--- Tweets ---")
    try:
        tweets = model.listTweets(token)
        for t in tweets:
            ref = f"(retweet de {t['ref_id']})" if t.get("ref_id") else ""
            print(f"[{t['nick']}] {t['content']} {ref} (ID: {t['id']})")
    except Exception as e:
        print("Error:", e)

def like_tweet():
    tweet_id = input("ID del tweet a likear: ")
    try:
        res = model.like(token, tweet_id)
        print("Like:", res)
    except Exception as e:
        print("Error:", e)

def dislike_tweet():
    tweet_id = input("ID del tweet a dislikear: ")
    try:
        res = model.dislike(token, tweet_id)
        print("Dislike:", res)
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
        choice = input("Opción: ").strip()
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
