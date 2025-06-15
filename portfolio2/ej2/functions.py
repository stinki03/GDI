import os
import pprint
import json

def clear_system(function):  
    def wrap(*args, **kwargs):
        os.system('clear')
        result = function(*args, **kwargs)
        input('')
        os.system('clear')
    wrap.__doc__ = function.__doc__
    return wrap

def show_user(user):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(user)

def get_address():
    street = input("Street: ")
    district = input("District: ")
    city = input("City: ")
    zip_code = input("Zip code: ")
    address = dict(street=street, district=district, city=city, zip_code=zip_code)
    return address

@clear_system
def create_user(db, r):
    """Crear un usuario nuevo"""
    username = input('Username: ')
    age = int(input('Age: '))
    email = input('Email: ')

    user = dict(username=username, age=age, email=email)

    address = input('Do you want to enter an address? (y/n) ').lower()
    if address == 'y':
        user['address'] = get_address()

    # Guardar el usuario en LevelDB como JSON
    db.put(username.encode(), json.dumps(user).encode())
    show_user(user)
    return user

def get_all_users(db):
    users = []
    for key, value in db:
        user = json.loads(value.decode())
        users.append(user)
    return users

def show_all_users(users):
    for user in users:
        pprint.pprint(user)

def get_all(db, r):
    """Mostrar todos los usuarios"""
    os.system("clear")
    users = get_all_users(db)
    show_all_users(users)
    input("Press Enter to continue.")

@clear_system
def get_user(db, r):
    """Obtener información de un usuario"""
    username = input('Username: ')
    data = db.get(username.encode())
    if data:
        user = json.loads(data.decode())
        show_user(user)
        return user
    else:
        print("Usuario no encontrado.")

@clear_system
def delete_user(db, r):
    """Eliminar un usuario"""
    username = input('Username: ')
    if db.get(username.encode()):
        db.delete(username.encode())
        print("Usuario eliminado.")
        return True
    else:
        print("Usuario no encontrado.")
        return False

@clear_system
def update_user(db, r):
    """Actualizar un usuario"""
    username = input('Username: ')
    data = db.get(username.encode())
    if not data:
        print("Usuario no encontrado.")
        return False

    user = json.loads(data.decode())
    answer = input('¿Actualizar el username? (y/n) ').lower()
    if answer == 'y':
        new_username = input('Nuevo username: ')
        user['username'] = new_username
        db.delete(username.encode())
        username = new_username

    answer = input('¿Actualizar la edad? (y/n) ').lower()
    if answer == 'y':
        user['age'] = int(input('Nueva edad: '))

    answer = input('¿Actualizar el email? (y/n) ').lower()
    if answer == 'y':
        user['email'] = input('Nuevo email: ')

    db.put(username.encode(), json.dumps(user).encode())
    print("Usuario actualizado.")
    return True

def default(*args, **kwargs):
    print("No es una opción válida.")