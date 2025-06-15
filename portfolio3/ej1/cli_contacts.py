
import sys, requests
BASE = "http://localhost:5000/contacts"
def create(name):
 r = requests.post(BASE, json={"name": name})
 print(r.json())
def list_all():
 r = requests.get(BASE)
 print(r.json())
def update(id, name):
 r = requests.put(f"{BASE}/{id}", json={"name": name})
 print(r.json())
def delete(id):
 r = requests.delete(f"{BASE}/{id}")
 print(r.status_code)
cmd = sys.argv[1]
if cmd == "create": create(sys.argv[2])
elif cmd == "list": list_all()
elif cmd == "update": update(sys.argv[2], sys.argv[3])
elif cmd == "delete": delete(sys.argv[2])
