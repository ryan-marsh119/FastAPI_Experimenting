from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends, APIRouter
from fastapi.responses import StreamingResponse
from app.schemas import UserRead, UserCreate, UserUpdate
from app.db import create_db_and_tables, get_async_session, Caught_Pokemon
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select
import shutil
import os
import uuid
import tempfile
from app.users import auth_backend, current_active_user, fastapi_users
import httpx
from starlette.background import BackgroundTask


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

@app.get("/pokemon")
async def get_pokemon():
    url = 'http://localhost/api/pokemon/'
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()

            if response.status_code == 200:
                data = response.json()
                return {'data': data}
        
        except Exception as e:
            raise HTTPException(status_code=response.status_code, detail=str(e))
            
  
@app.get("/pokemon/{id}")
async def get_pokemon(id: int):
    url = 'http://localhost/api/pokemon/' + str(id) + "/"
    async with httpx.AsyncClient() as client:
        try:
            print("Inside try")
            response = await client.get(url)
            response.raise_for_status()

            if response.status_code == 200:
                data = response.json()
                return {'data': data}
            
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))