from pymongo import MongoClient
from functions import *

if __name__ == '__main__':
    client = MongoClient()
    database = client['mydb']
    collection = database['users']
    
    options = {
        "1": create_user,
        "2": get_user,
        "3": get_all,
        "4": delete_user,
        "5": update_user
        }


    while True:
        for key, function in options.items():
            print(f"{key}.", function.__doc__)

        option = input("Select the number for an option (q or quit to exit): ").lower()

        if option == "q" or option == "quit":
            break

        function_selected = options.get(option, default)
        function_selected(collection)
