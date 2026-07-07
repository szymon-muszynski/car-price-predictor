from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import joblib
from pathlib import Path
from routers import predictions

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

MODEL_PATH = "car_price_model_500_pages.pkl"
COLUMNS_PATH = "model_columns_500_pages.pkl"

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("⏳ Ładowanie modelu wyceny do pamięci RAM...")
    app.state.car_model = joblib.load(DATA_DIR / MODEL_PATH)
    app.state.model_columns = joblib.load(DATA_DIR / COLUMNS_PATH)
    print("✅ Serwer i AI gotowe do wyceny aut!")
    
    yield 
    
    print("🔴 Zamykanie serwera, zwalnianie pamięci...")
    del app.state.car_model
    del app.state.model_columns

app = FastAPI(lifespan=lifespan)

app.include_router(predictions.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
