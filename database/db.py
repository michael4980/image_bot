from database.models import *
from database.config import load_config

config = load_config(r'database/source.ini')

db.bind(provider='postgres', host=config.db.host, user=config.db.user, 
        password=config.db.password, database=config.db.database)
db.generate_mapping(create_tables=True)