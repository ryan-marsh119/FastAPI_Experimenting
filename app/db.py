from collections.abc import AsyncGenerator
import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, SmallInteger, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime
import os
from dotenv import load_dotenv
from fastapi_users.db import SQLAlchemyUserDatabase, SQLAlchemyBaseUserTableUUID
from fastapi import Depends

load_dotenv()

username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")

DATABASE_URL = f"postgresql+asyncpg://{username}:{password}@{host}"

class Base(DeclarativeBase):
    pass

class User(SQLAlchemyBaseUserTableUUID, Base):
    pass
#     __tablename__ = 'trainer'

#     # team_id = Column(UUID(as_uuid=True), ForeignKey("team.id"), nullable=False)
#     # team_count = Column(SmallInteger, default=0)

#     team = relationship("Caught_Pokemon", back_populates="trainer")

#     pokecenter = relationship("Pokecenter", back_populates="trainer")

class Caught_Pokemon(Base):
    __tablename__ = 'caught_pokemon'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    type1 = Column(String, nullable=False)
    type2 = Column(String)
    hp = Column(Integer)
    attack = Column(Integer)
    defense = Column(Integer)
    special_attack = Column(Integer)
    speed = Column(Integer)
    generation = (SmallInteger)
    legendary = Column(Boolean, default=False)

    # trainer_id =Column(UUID(as_uuid=True), ForeignKey("trainer.id"), nullable=False)
    # count = Column(SmallInteger, primary_key=True, max_value=6)

    # trainer = relationship("Trainer", back_populates="caught_pokemon")



# class Pokecenter(Base):

#     __tablename__ = 'pokecenter'

#     id = Column(UUID(as_uuid=True), )

#     trainer = relationship("Trainer", back_populates="pokecenter")

    # posts = relationship("Post", back_populates="user")

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, Trainer)