from pymongo import MongoClient
from functions import *

def main():
    client = MongoClient()
    database = client['mydb']
    users_collection = database['users']

    options = {
        "1": create_user,
        "2": get_user,
        "3": get_all,
        "4": delete_user,
        "5": update_user,
        "6": add_contact,
        "7": get_contacts,
        "8": update_contact,
        "9": delete_contact
    }

    while True:
        print("\nOpciones:")
        print("1. Crear usuario")
        print("2. Ver usuario")
        print("3. Ver todos los usuarios")
        print("4. Eliminar usuario")
        print("5. Actualizar usuario")
        print("6. Agregar contacto a usuario")
        print("7. Ver contactos de un usuario")
        print("8. Actualizar un contacto de usuario")
        print("9. Eliminar un contacto de usuario")
        print("q. Salir")

        option = input("Selecciona el número de una opción (q o quit para salir): ").lower()

        if option in ("q", "quit"):
            print("Saliendo del programa.")
            break

        function_selected = options.get(option, default)
        function_selected(users_collection)

if __name__ == '__main__':
    main()
