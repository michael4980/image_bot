import pydantic
from datetime import datetime


class Customer(pydantic.BaseModel):
    nick : str = None
    tg_id : str 


class Logger(pydantic.BaseModel):
    create_date : datetime = None
    operation : str
    size : int
    image_name : str
    user : Customer = None
    
class Log_create(pydantic.BaseModel):
    operation : str
    size : int
    image_name : str
    tg_id : str
    
Logger.update_forward_refs()
Log_create.update_forward_refs()
Customer.update_forward_refs()