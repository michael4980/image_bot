from datetime import datetime
import sys
from database.db import *


sys.path.insert(1, r'C:\Users\USER\Desktop\python_projects\my_projects\something')
import pydantic_models

@db_session
def create_customer(tg_id: str, nick: str = None):
    if nick:
        user = Customer(tg_id=tg_id, nick=nick)
    else:
        user = Customer(tg_id=tg_id)
    flush()     
    return user

@db_session
def create_operation(operation_log: str, size: int, image_name:str, tg_id : str):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user = get_user_by_tg_id(tg_id)
    fin = user if user else create_customer(tg_id)
    log = Logger(create_date = time, operation = operation_log,
                 size = size, image_name = image_name, user = fin)
    return log

@db_session
def get_user_info(tg_id: str):
    result = get_user_by_tg_id(tg_id)
    cust, id = result, result.id
    return {'id': cust.id,
            'nick': cust.nick,
            'tg_id': cust.tg_id,
            'num_of_operations': list(select((c.user, count(c.user, distinct = False)) 
                                             for c in Logger if cust.id == id).filter(lambda c, x: c == Customer[id]))[0][1]}

@db_session
def get_user_by_tg_id(tg_id: str):
    return Customer.select(lambda u: u.tg_id == tg_id).first() if Customer.tg_id else None

@db_session
def get_operation_info(log: pydantic_models.Logger):
    log = Logger[log]
    result = Customer.select(lambda cus: cus.id == log.user.id).first() 
    return {'date': log.create_date,
            'operation': log.operation,
            'size': log.size,
            'image_name': log.image_name,
            'user_id': result.tg_id}







