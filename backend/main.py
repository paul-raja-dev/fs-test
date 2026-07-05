from fastapi import FastAPI,Depends
from database import get_db
import models
import schemas
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.post("/login")
async def create_user(user: schemas.CreateUser , db: AsyncSession = Depends(get_db)):

    # db_user = await db.execute(select(models.User).filter(models.User.username == user.username))
    # if db_user:
    #     return JSONResponse({'msg':'user already exists'})

    new_user = models.User(
        username = user.username,
        password = user.password
    )
    
    db.add(new_user)
    await db.commit()
    return JSONResponse({'msg':'user created successfully'})
    

@app.get("/users")
async def display_user(db: AsyncSession = Depends(get_db)):

    users = await db.execute(select(models.User))
    users = users.scalars().all()

    return users



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)