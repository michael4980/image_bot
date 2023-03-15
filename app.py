import fastapi
import pydantic_models
import uvicorn
import database.crud as crud

api = fastapi.FastAPI()

@api.get("/users")
@crud.db_session
def get_users():
    users = []
    for user in crud.Customer.select()[:]:
        users.append(user.to_dict())
    return users

@api.get('/user_info/')
def get_user_info(user: pydantic_models.Customer):
    return crud.get_user_info(tg_id = user.tg_id)

@api.get('/oper_info/{id}')
def get_oper_info(id : int):
    return crud.get_operation_info(id)


@api.post('/user/create')
def create_user(user: pydantic_models.Customer):
    return crud.create_customer(tg_id=user.tg_id,
                            nick=user.nick).to_dict()
    
@api.post('/active_create')
def create_operation(log: pydantic_models.Log_create):
    return crud.create_operation(operation_log= log.operation, size= log.size, 
                                 image_name= log.image_name, tg_id= log.tg_id).to_dict()
    

def start_app():
    uvicorn.run("app:api", host = '127.0.0.1', port = 8000, reload = True)