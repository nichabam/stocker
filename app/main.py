from fastapi import FastAPI
from . import models
from .database import engine
from .routes import categories, items, stock_history, restock_history

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(categories.router)
app.include_router(items.router)
app.include_router(stock_history.router)
app.include_router(restock_history.router)

@app.get("/")
def home():
    return {"message": "Stocker is running w/ database"}