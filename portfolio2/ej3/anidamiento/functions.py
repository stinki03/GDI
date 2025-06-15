import os
import pprint
import uuid

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
def create_user(collection):
    """Crear usuario"""
    username = input('Username: ')
    age = int(input('Age: '))
    email = input('Email: ')
    user = dict(username=username, age=age, email=email, contacts=[])
    address = input('¿Quieres ingresar una dirección? (y/n) ').lower()
    if address == 'y':
        user['address'] = get_address()
    collection.insert_one(user)
    show_user(user)
    return user

def get_all(collection):
    """Ver todos los usuarios"""
    os.system("clear")
    for user in collection.find():
        pprint.pprint(user)
    input("Presiona Enter para continuar.")

@clear_system
def get_user(collection):
    """Ver un usuario"""
    username = input('Username: ')
    user = collection.find_one({'username': username}, {'_id': False})
    if user:
        show_user(user)
        return user
    else:
        print("No se pudo obtener ese usuario.")

@clear_system
def delete_user(collection):
    """Eliminar usuario"""
    username = input('Username: ')
    result = collection.delete_one({'username': username})
    print(result.acknowledged)
    return result.acknowledged

@clear_system
def update_user(collection):
    """Actualizar usuario"""
    username = input('Username: ')
    updated_user = {}
    answer = input('¿Actualizar username? (y/n) ').lower()
    if answer == 'y':
        new_username = input('Nuevo username: ')
        updated_user['username'] = new_username
    answer = input('¿Actualizar edad? (y/n) ').lower()
    if answer == 'y':
        new_age = int(input('Nueva edad: '))
        updated_user['age'] = new_age
    answer = input('¿Actualizar email? (y/n) ').lower()
    if answer == 'y':
        new_email = input('Nuevo email: ')
        updated_user['email'] = new_email
    result = collection.update_one({'username': username},{"$set": updated_user})
    print(result.acknowledged)
    return result.acknowledged

# CRUD de contactos con anidamiento explícito (contact_id)
@clear_system
def add_contact(collection):
    """Agregar contacto a un usuario"""
    username = input('Username del usuario: ')
    user = collection.find_one({'username': username})
    if not user:
        print("Usuario no encontrado.")
        return
    contact = {
        'contact_id': str(uuid.uuid4()),
        'name': input('Nombre del contacto: '),
        'phone': input('Teléfono: '),
        'email': input('Email: '),
        'relationship': input('Relación: ')
    }
    collection.update_one({'username': username}, {'$push': {'contacts': contact}})
    print(f"Contacto agregado con ID: {contact['contact_id']}")

@clear_system
def get_contacts(collection):
    """Ver contactos de un usuario"""
    username = input('Username del usuario: ')
    user = collection.find_one({'username': username}, {'contacts': 1, '_id': 0})
    if not user:
        print("Usuario no encontrado.")
        return
    contacts = user.get('contacts', [])
    if not contacts:
        print("No hay contactos.")
    else:
        for idx, contact in enumerate(contacts):
            print(f"Contacto #{idx+1} (ID: {contact['contact_id']}):")
            pprint.pprint(contact)

@clear_system
def update_contact(collection):
    """Actualizar contacto de un usuario"""
    username = input('Username del usuario: ')
    user = collection.find_one({'username': username})
    if not user or not user.get('contacts'):
        print("Usuario o contactos no encontrados.")
        return
    for idx, contact in enumerate(user['contacts']):
        print(f"{idx+1}. {contact['name']} (ID: {contact['contact_id']})")
    contact_id = input("Introduce el contact_id del contacto a actualizar: ").strip()
    contacts = user['contacts']
    for i, contact in enumerate(contacts):
        if contact['contact_id'] == contact_id:
            updated_contact = contact.copy()
            for key in ['name', 'phone', 'email', 'relationship']:
                answer = input(f"¿Actualizar {key}? (y/n) ").lower()
                if answer == 'y':
                    updated_contact[key] = input(f"Nuevo {key}: ")
            contacts[i] = updated_contact
            collection.update_one({'username': username}, {'$set': {'contacts': contacts}})
            print("Contacto actualizado.")
            return
    print("No se encontró el contact_id.")

@clear_system
def delete_contact(collection):
    """Eliminar contacto de un usuario"""
    username = input('Username del usuario: ')
    user = collection.find_one({'username': username})
    if not user or not user.get('contacts'):
        print("Usuario o contactos no encontrados.")
        return
    for idx, contact in enumerate(user['contacts']):
        print(f"{idx+1}. {contact['name']} (ID: {contact['contact_id']})")
    contact_id = input("Introduce el contact_id del contacto a eliminar: ").strip()
    contacts = user['contacts']
    new_contacts = [c for c in contacts if c['contact_id'] != contact_id]
    if len(new_contacts) == len(contacts):
        print("No se encontró el contact_id.")
        return
    collection.update_one({'username': username}, {'$set': {'contacts': new_contacts}})
    print("Contacto eliminado.")

def default(*args, **kwargs):
    print("No es una opción válida.")
