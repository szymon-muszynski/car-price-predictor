from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import joblib
from pathlib import Path
from routers import predictions
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
KNN_DIR = DATA_DIR / "kNN_model"

MODEL_PATH = "car_price_model_500_pages.pkl"
COLUMNS_PATH = "model_columns_500_pages.pkl"

KNN_MODEL_PATH = "knn_model_similar_cars.pkl"
KNN_SCALER_PATH = "knn_scaler.pkl"
KNN_COLUMNS_PATH = "knn_columns.pkl"
KNN_DF_REF_PATH = "df_ref_similar_cars.pkl"

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("⏳ Ładowanie modelu wyceny do pamięci RAM...")
    app.state.car_model = joblib.load(DATA_DIR / MODEL_PATH)
    app.state.model_columns = joblib.load(DATA_DIR / COLUMNS_PATH)
    
    print("⏳ Ładowanie bazy kNN i algorytmów rekomendacyjnych...")
    app.state.knn_model = joblib.load(KNN_DIR / KNN_MODEL_PATH)
    app.state.knn_scaler = joblib.load(KNN_DIR / KNN_SCALER_PATH)
    app.state.knn_columns = joblib.load(KNN_DIR / KNN_COLUMNS_PATH)
    app.state.df_ref = pd.read_pickle(KNN_DIR / KNN_DF_REF_PATH)
    
    print("✅ Serwer i AI gotowe do wyceny aut!")
    
    yield 
    
    print("🔴 Zamykanie serwera, zwalnianie pamięci...")
    app.state.car_model = None
    app.state.knn_model = None
    app.state.df_ref = None

app = FastAPI(lifespan=lifespan)

app.include_router(predictions.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
