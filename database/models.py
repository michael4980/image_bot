from datetime import datetime
from pony.orm import *
from database.config import load_config

config = load_config(r'database/source.ini')

db = Database()


class Customer(db.Entity):
    id = PrimaryKey(int, auto=True)
    nick = Optional(str, 50)
    tg_id = Required(str, 30, unique=True)
    log = Set('Logger')


class Logger(db.Entity):
    id = PrimaryKey(int, auto=True)
    create_date = Required(datetime)
    operation = Required(str, 20)
    size = Required(int)
    image_name = Optional(str, 50)
    user = Required(Customer)


