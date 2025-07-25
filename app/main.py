from fastapi import FastAPI
from . import models
from .database import engine
from .routes import categories

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(categories.router)

@app.get("/")
def home():
    return {"message": "Stocker is running w/ database"}