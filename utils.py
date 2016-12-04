import json
config = json.load(open('config.json', 'r'))

def is_admin(data):
    password = data.get("password")
    if not password:
        return False
    for admin in config['admins']:
        if admin.get('password') == password:
            return True
    return False

def get_admin_logins():
    return [ admin['login'] for admin in config['admins']]
 
