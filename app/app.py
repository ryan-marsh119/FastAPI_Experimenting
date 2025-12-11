from fastapi import FastAPI, HTTPException,  UploadFile, Depends, Form
from app.schemas import UserRead, UserCreate, UserUpdate, Pokemon, NewPokemon
from app.db import create_db_and_tables, get_async_session, CaughtPokemon, User
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select, update
from app.users import auth_backend, current_active_user, fastapi_users
from typing import Annotated

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(fastapi_users.get_auth_router(auth_backend), prefix='/auth/jwt', tags=["auth"])
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_reset_password_router(), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_verify_router(UserRead), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_users_router(UserRead, UserUpdate), prefix="/users", tags=["users"])

@app.get("/pokedex")
async def get_pokedex(page: int = 1, db: AsyncSession = Depends(get_async_session)):
    limit = 3
    offset = (page - 1) * limit
    stmt = select(CaughtPokemon).limit(limit).offset(offset)
    result = await db.scalars(stmt)
    pokemon = result.all()
    return [Pokemon.model_validate(p, from_attributes=True) for p in pokemon]
  
@app.get("/pokedex/{id}")
async def get_pokedex(id: int, db: AsyncSession = Depends(get_async_session)):
    stmt = select(CaughtPokemon).where(CaughtPokemon.id == id)
    result = await db.scalars(stmt)
    pokemon = result.one_or_none()

    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokemon not found!")

    return Pokemon.model_validate(pokemon, from_attributes=True)
        

@app.post("/pokedex")
async def catch_pokemon(
    pokemon: NewPokemon,
    user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_async_session)
):
    try:
        new_pokemon = CaughtPokemon(
            trainer_id = user.id,
            **pokemon.model_dump()
        )
        db.add(new_pokemon)
        await db.commit()
        await db.refresh(new_pokemon)
        return Pokemon.model_validate(new_pokemon, from_attributes=True)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/pokedex/{id}")
async def delete_pokemon(
    id: int,
    user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_async_session)
):
    stmt = select(CaughtPokemon).where(CaughtPokemon.id == id)
    result = await db.scalars(stmt)
    deleted_pokemon = result.one_or_none()

    if not deleted_pokemon:
        raise HTTPException(status_code=404, detail="Pokemon not found. Delete unsuccessful.")
    
    if deleted_pokemon.trainer_id != user.id:
        raise HTTPException(status_code=401, detail="Unauthorized! Thats not your pokemon!")
    
    await db.delete(deleted_pokemon)
    await db.commit()

@app.put("/pokedex/")
async def update_pokemon_name(
    id: int,
    name: Annotated[str, Form()],
    user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_async_session),
):
    stmt = select(CaughtPokemon).where(CaughtPokemon.id == id)
    result = await db.scalars(stmt)
    pokemon = result.one_or_none()

    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokemon not found!")
    
    if pokemon.trainer_id != user.id:
        raise HTTPException(status_code=401, details="Not authorized.")
 
    await db.execute(update(CaughtPokemon), [{"id":id, "name": name}],)
    await db.commit()

    return Pokemon.model_validate(pokemon, from_attributes=True)
