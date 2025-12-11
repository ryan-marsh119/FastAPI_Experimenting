from pydantic import BaseModel
from fastapi_users import schemas
import uuid
from sqlalchemy.sql.sqltypes import SmallInteger

class UserRead(schemas.BaseUser[uuid.UUID]):
    pass
    
class UserCreate(schemas.BaseUserCreate):
    pass

class UserUpdate(schemas.BaseUserUpdate):
    pass

class NewPokemon(BaseModel):

    id : int
    name : str
    type1 : str
    type2 : str | None = None
    total : int
    hp : int
    attack : int
    defense : int
    special_attack : int
    special_defense : int
    speed : int
    generation : int
    legendary : bool

class Pokemon(NewPokemon):
    trainer_id : uuid.UUID