from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routes import categories, items, stock_history, restock_history, analytics, auth

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

models.Base.metadata.create_all(bind=engine)

app.include_router(categories.router)
app.include_router(items.router)
app.include_router(stock_history.router)
app.include_router(restock_history.router)
app.include_router(analytics.router)
app.include_router(auth.router)

@app.get("/")
def home():
    return {"message": "Stocker is running w/ database"}