from fastapi import APIRouter, HTTPException, Depends
from ..db import CaughtPokemon, User, get_async_session
from ..schemas import Pokemon, NewPokemon, UpdatePokemon
from ..users import current_active_user
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/pokedex",
    tags=["pokemon"],
)

@router.get("/")
async def get_pokedex(
    db: AsyncSession = Depends(get_async_session),
    page: int = 1
) -> list[Pokemon]:
    limit = 5
    offset = (page - 1) * limit
    stmt = select(CaughtPokemon).limit(limit).offset(offset)
    result = await db.scalars(stmt)
    pokemon = result.all()
    return [Pokemon.model_validate(p, from_attributes=True) for p in pokemon]
  
@router.get("/{id}")
async def get_pokedex(
        id: int,
        db: AsyncSession = Depends(get_async_session)
) -> Pokemon:
    stmt = select(CaughtPokemon).where(CaughtPokemon.id == id)
    result = await db.scalars(stmt)
    pokemon = result.one_or_none()

    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokemon not found!")

    return Pokemon.model_validate(pokemon, from_attributes=True)
        
@router.post("/catch")
async def catch_pokemon(
    pokemon: NewPokemon,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
) -> Pokemon:
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

@router.delete("/{id}")
async def delete_pokemon(
    id: int,
    user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_async_session)
) -> None:
    stmt = select(CaughtPokemon).where(CaughtPokemon.id == id)
    result = await db.scalars(stmt)
    deleted_pokemon = result.one_or_none()

    if not deleted_pokemon:
        raise HTTPException(status_code=404, detail="Pokemon not found. Delete unsuccessful.")
    
    if deleted_pokemon.trainer_id != user.id:
        raise HTTPException(status_code=401, detail="Unauthorized! Thats not your pokemon!")
    
    await db.delete(deleted_pokemon)
    await db.commit()

@router.patch("/{id}")
async def update_pokemon_name(
    id: int,
    pokemon_data: UpdatePokemon,
    user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_async_session),
) -> Pokemon:
    stmt = select(CaughtPokemon).where(CaughtPokemon.id == id)
    result = await db.execute(stmt)
    db_result = result.scalar_one_or_none()

    if not db_result:
        raise HTTPException(status_code=404, detail="Pokemon not found.")
    
    if db_result.trainer_id != user.id:
        raise HTTPException(status_code=401, detail="Not your pokemon. Unauthorized.")

    update_data = pokemon_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_result, key, value)
    
    await db.commit()
    await db.refresh(db_result)

    return Pokemon.model_validate(db_result, from_attributes=True)