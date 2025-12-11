from collections.abc import AsyncGenerator
from sqlalchemy import Column, String, ForeignKey, SmallInteger, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship
from fastapi_users.db import SQLAlchemyUserDatabase, SQLAlchemyBaseUserTableUUID
from fastapi import Depends
from app.settings import DATABASE_URL

class Base(DeclarativeBase):
    pass

class User(SQLAlchemyBaseUserTableUUID, Base):
    caught_pokemon = relationship("CaughtPokemon", back_populates="trainer")

class CaughtPokemon(Base):
    __tablename__ = 'caught_pokemon'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    type1 = Column(String, nullable=False)
    type2 = Column(String, nullable=True, default=None)
    total = Column(Integer)
    hp = Column(Integer)
    attack = Column(Integer)
    defense = Column(Integer)
    special_attack = Column(Integer)
    special_defense = Column(Integer)
    speed = Column(Integer)
    generation = Column(SmallInteger)
    legendary = Column(Boolean, default=False)
    trainer_id =Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)

    trainer = relationship("User", back_populates="caught_pokemon")

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)