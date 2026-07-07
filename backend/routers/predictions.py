from fastapi import APIRouter, Request, HTTPException, Depends
from schemas import CarPredictionRequest, CarPredictionResponse
from prediction import predict_car_price

router = APIRouter(prefix="/api/predictions", tags=["Wycena Samochodów AI"])

def get_ml_model(request: Request):
    return request.app.state.car_model

def get_model_columns(request: Request):
    return request.app.state.model_columns

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