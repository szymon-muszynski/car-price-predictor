from fastapi import APIRouter, Request, HTTPException, Depends
from schemas import CarPredictionRequest, CarPredictionResponse, SimilarCarsListResponse
from prediction import predict_car_price, find_similar_cars

router = APIRouter(prefix="/api/predictions", tags=["Wycena Samochodów AI"])

def get_ml_model(request: Request):
    return request.app.state.car_model

def get_model_columns(request: Request):
    return request.app.state.model_columns

def get_knn_model(request: Request): return request.app.state.knn_model
def get_knn_scaler(request: Request): return request.app.state.knn_scaler
def get_knn_columns(request: Request): return request.app.state.knn_columns
def get_df_ref(request: Request): return request.app.state.df_ref

@router.post("/price", response_model=CarPredictionResponse)
def get_price_prediction(
    payload: CarPredictionRequest, 
    prediction_model = Depends(get_ml_model),
    model_columns = Depends(get_model_columns)
):
    try:
        price = predict_car_price(payload.model_dump(), prediction_model, model_columns)
        
        return CarPredictionResponse(
            predicted_price=round(price, 2)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd podczas wyceny modelu: {str(e)}")
    
@router.post("/similar", response_model=SimilarCarsListResponse)
def get_similar_cars_endpoint(
    payload: CarPredictionRequest,
    knn_model = Depends(get_knn_model),
    knn_scaler = Depends(get_knn_scaler),
    knn_columns = Depends(get_knn_columns),
    df_ref = Depends(get_df_ref)
):
    try:
        similar_cars = find_similar_cars(
            payload.model_dump(), 
            knn_model, 
            knn_scaler, 
            knn_columns, 
            df_ref
        )
        return SimilarCarsListResponse(similar_cars=similar_cars)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd podczas wyszukiwania podobnych ofert: {str(e)}")