from pydantic import BaseModel
from typing import List

class CarPredictionRequest(BaseModel):
    przebieg: int
    pojemnosc_skokowa: int
    moc: int
    wiek: int
    rodzaj_paliwa: str      
    skrzynia_biegow: str    
    marka: str              

class CarPredictionResponse(BaseModel):
    predicted_price: float
    currency: str = "PLN"
    
class SimilarCar(BaseModel):
    tytul: str
    cena: float
    rocznik: int
    przebieg: int
    moc: int
    pojemnosc_skokowa: int
    url: str

class SimilarCarsListResponse(BaseModel):
    similar_cars: List[SimilarCar]