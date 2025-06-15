import redis
import plyvel
from functions import *

def main():
    # Conexión a Redis
    r = redis.Redis(host='localhost', port=6379, db=0)
    # Conexión a LevelDB
    db = plyvel.DB('mydb/', create_if_missing=True)

    options = {
        "1": create_user,
        "2": get_user,
        "3": get_all,
        "4": delete_user,
        "5": update_user,
    }

    while True:
        print("\nOpciones:")
        for key, function in options.items():
            print(f"{key}. {function.__doc__}")

        option = input("Selecciona el número de una opción (q o quit para salir): ").lower()

        if option in ("q", "quit"):
            print("Saliendo del programa.")
            break

        function_selected = options.get(option, default)
        function_selected(db, r)

    db.close()

if __name__ == '__main__':
    main()