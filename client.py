import requests
from database import config

conf = config.load_config(r'database/source.ini')

api_url = conf.tg_bot.api_url

def get_users():
    return requests.get(f"{api_url}/users").json()

def get_user_by_id(tg_id):
    info = {"tg_id" : tg_id}
    return requests.get(f"{api_url}/user_info/", json = info).json()

def create_operation(log, tg_id, size, image_name):
    info = {"operation" : log, 
            "size" : size, 
            "image_name" : image_name, 
            "tg_id" : tg_id}
    return requests.post(f"{api_url}/active_create/", json=info).json()

def user_create(tg_id, nick):
    info = {"tg_id": tg_id,
            "nick": nick}
    return requests.post(f"{api_url}/user/create/", json=info).json()
