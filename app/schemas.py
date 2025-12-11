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

class UpdatePokemon(BaseModel):
    name : str | None = None
    type1 : str | None = None
    type2 : str | None = None
    total : int | None = None
    hp : int | None = None
    attack : int | None = None
    defense : int | None = None
    special_attack : int | None = None
    special_defense : int | None = None
    speed : int | None = None
    generation : int | None = None
    legendary : bool | None = None

class ResponsePokemon(NewPokemon):
    class Config:
        from_attributes = True

class Pokemon(NewPokemon):
    trainer_id : uuid.UUID
    id : int