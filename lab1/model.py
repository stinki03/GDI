import mysql.connector
import uuid
import time

def init():
    con = None
    cur = None
    try:
        con = mysql.connector.connect(
            user="root",
            password="root",
            host="localhost",  # Cambia esto si usas otro host
            port="3306"
        )
        cur = con.cursor()
        cur.execute("CREATE DATABASE IF NOT EXISTS twitter")
        cur.execute("USE twitter")
        # Tabla Users
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                id CHAR(32) PRIMARY KEY,
                name VARCHAR(50),
                surname VARCHAR(50),
                email VARCHAR(100) UNIQUE,
                password VARCHAR(100),
                nick VARCHAR(50) UNIQUE
            )
        """)
        # Tabla Tweets
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Tweets (
                id CHAR(32) PRIMARY KEY,
                user_id CHAR(32),
                date BIGINT,
                content VARCHAR(280),
                ref_id CHAR(32),
                FOREIGN KEY (user_id) REFERENCES Users(id),
                FOREIGN KEY (ref_id) REFERENCES Tweets(id)
            )
        """)
        # Tabla Following
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Following (
                follower_id CHAR(32),
                followed_id CHAR(32),
                PRIMARY KEY (follower_id, followed_id),
                FOREIGN KEY (follower_id) REFERENCES Users(id),
                FOREIGN KEY (followed_id) REFERENCES Users(id)
            )
        """)
        # Tabla Likes
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Likes (
                user_id CHAR(32),
                tweet_id CHAR(32),
                PRIMARY KEY (user_id, tweet_id),
                FOREIGN KEY (user_id) REFERENCES Users(id),
                FOREIGN KEY (tweet_id) REFERENCES Tweets(id)
            )
        """)
        # Tabla Dislikes
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Dislikes (
                user_id CHAR(32),
                tweet_id CHAR(32),
                PRIMARY KEY (user_id, tweet_id),
                FOREIGN KEY (user_id) REFERENCES Users(id),
                FOREIGN KEY (tweet_id) REFERENCES Tweets(id)
            )
        """)
        con.commit()
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        if cur is not None:
            cur.close()
        if con is not None and con.is_connected():
            con.close()

# Inicializar base de datos al cargar el módulo
init()

def get_connection():
    return mysql.connector.connect(
        user="root",
        password="root",
        host="localhost",  # Cambia esto si usas otro host
        port="3306",
        database="twitter"
    )

# Simulación de autenticación: el "token" será el id del usuario
def addUser(user):
    if not all(k in user for k in ["name", "surname", "email", "password", "nick"]):
        raise Exception("Missing required fields")
    user["id"] = uuid.uuid4().hex
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute("SELECT * FROM Users WHERE email=%s OR nick=%s", (user["email"], user["nick"]))
        if cur.fetchall():
            raise Exception("User already exists")
        cur.execute("""
            INSERT INTO Users (id, name, surname, email, password, nick)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (user["id"], user["name"], user["surname"], user["email"], user["password"], user["nick"]))
        con.commit()
        return user
    finally:
        con.close()

def login(email, password):
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute("SELECT id FROM Users WHERE email=%s AND password=%s", (email, password))
        row = cur.fetchone()
        if not row:
            raise Exception("Invalid email or password")
        user_id = row[0]
        return user_id
    finally:
        con.close()

def listUsers(token, query=""):
    con = get_connection()
    try:
        cur = con.cursor(dictionary=True)
        if query:
            cur.execute("SELECT name, surname, email, nick FROM Users WHERE name LIKE %s OR surname LIKE %s OR email LIKE %s OR nick LIKE %s", 
                        (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%"))
        else:
            cur.execute("SELECT name, surname, email, nick FROM Users")
        return [dict(row) for row in cur.fetchall()]
    finally:
        con.close()

def updateUser(token, user):
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute("UPDATE Users SET name=%s, surname=%s, email=%s, password=%s, nick=%s WHERE id=%s",
                    (user["name"], user["surname"], user["email"], user["password"], user["nick"], token))
        con.commit()
        return True
    finally:
        con.close()

def removeUser(token):
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM Users WHERE id=%s", (token,))
        con.commit()
        return True
    finally:
        con.close()

def follow(token, nick):
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute("SELECT id FROM Users WHERE nick=%s", (nick,))
        row = cur.fetchone()
        if not row:
            raise Exception("User not found")
        followed_id = row[0]
        cur.execute("INSERT IGNORE INTO Following (follower_id, followed_id) VALUES (%s, %s)", (token, followed_id))
        con.commit()
        return True
    finally:
        con.close()

def unfollow(token, nick):
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute("SELECT id FROM Users WHERE nick=%s", (nick,))
        row = cur.fetchone()
        if not row:
            raise Exception("User not found")
        followed_id = row[0]
        cur.execute("DELETE FROM Following WHERE follower_id=%s AND followed_id=%s", (token, followed_id))
        con.commit()
        return True
    finally:
        con.close()

def listFollowing(token, query=""):
    con = get_connection()
    try:
        cur = con.cursor(dictionary=True)
        q = """
            SELECT u.name, u.surname, u.email, u.nick
            FROM Users u
            JOIN Following f ON f.followed_id = u.id
            WHERE f.follower_id = %s
        """
        params = [token]
        if query:
            q += " AND (u.name LIKE %s OR u.surname LIKE %s OR u.email LIKE %s OR u.nick LIKE %s)"
            params += [f"%{query}%"]*4
        cur.execute(q, params)
        return [dict(row) for row in cur.fetchall()]
    finally:
        con.close()

def listFollowers(token, query=""):
    con = get_connection()
    try:
        cur = con.cursor(dictionary=True)
        q = """
            SELECT u.name, u.surname, u.email, u.nick
            FROM Users u
            JOIN Following f ON f.follower_id = u.id
            WHERE f.followed_id = %s
        """
        params = [token]
        if query:
            q += " AND (u.name LIKE %s OR u.surname LIKE %s OR u.email LIKE %s OR u.nick LIKE %s)"
            params += [f"%{query}%"]*4
        cur.execute(q, params)
        return [dict(row) for row in cur.fetchall()]
    finally:
        con.close()

def addTweet(token, content):
    twid = uuid.uuid4().hex
    date = int(time.time())
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute("INSERT INTO Tweets (id, user_id, date, content, ref_id) VALUES (%s, %s, %s, %s, NULL)",
                    (twid, token, date, content))
        con.commit()
        return {"id": twid, "content": content}
    finally:
        con.close()

def addRetweet(token, tweet_id):
    twid = uuid.uuid4().hex
    date = int(time.time())
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute("SELECT id FROM Tweets WHERE id=%s", (tweet_id,))
        if not cur.fetchone():
            raise Exception("Original tweet not found")
        cur.execute("INSERT INTO Tweets (id, user_id, date, content, ref_id) VALUES (%s, %s, %s, '', %s)",
                    (twid, token, date, tweet_id))
        con.commit()
        return {"id": twid, "ref_id": tweet_id}
    finally:
        con.close()

def listTweets(token, query=""):
    con = get_connection()
    try:
        cur = con.cursor(dictionary=True)
        q = "SELECT t.id, t.content, t.date, t.ref_id, u.nick FROM Tweets t JOIN Users u ON t.user_id=u.id"
        params = []
        if query:
            q += " WHERE t.content LIKE %s"
            params.append(f"%{query}%")
        q += " ORDER BY t.date DESC"
        cur.execute(q, params)
        return [dict(row) for row in cur.fetchall()]
    finally:
        con.close()

def like(token, tweet_id):
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute("INSERT IGNORE INTO Likes (user_id, tweet_id) VALUES (%s, %s)", (token, tweet_id))
        cur.execute("DELETE FROM Dislikes WHERE user_id=%s AND tweet_id=%s", (token, tweet_id))
        con.commit()
        return True
    finally:
        con.close()

def dislike(token, tweet_id):
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute("INSERT IGNORE INTO Dislikes (user_id, tweet_id) VALUES (%s, %s)", (token, tweet_id))
        cur.execute("DELETE FROM Likes WHERE user_id=%s AND tweet_id=%s", (token, tweet_id))
        con.commit()
        return True
    finally:
        con.close()

def listLikes(token, tweet_id):
    con = get_connection()
    try:
        cur = con.cursor(dictionary=True)
        cur.execute("""
            SELECT u.name, u.surname, u.email, u.nick
            FROM Users u
            JOIN Likes l ON l.user_id = u.id
            WHERE l.tweet_id = %s
        """, (tweet_id,))
        return [dict(row) for row in cur.fetchall()]
    finally:
        con.close()

def listDislikes(token, tweet_id):
    con = get_connection()
    try:
        cur = con.cursor(dictionary=True)
        cur.execute("""
            SELECT u.name, u.surname, u.email, u.nick
            FROM Users u
            JOIN Dislikes d ON d.user_id = u.id
            WHERE d.tweet_id = %s
        """, (tweet_id,))
        return [dict(row) for row in cur.fetchall()]
    finally:
        con.close()