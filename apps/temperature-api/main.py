from fastapi import FastAPI, Query, Path, HTTPException
from pydantic import BaseModel
from datetime import datetime
import random

app = FastAPI(title="Temperature API (Python)", version="1.0.0")


class TemperatureData(BaseModel):
    value: float
    unit: str
    timestamp: datetime
    location: str
    status: str
    sensor_id: str
    sensor_type: str
    description: str


def generate_temperature_data(location: str, sensor_id: str) -> TemperatureData:
    value = 18.0 + (random.randint(0, 10) + random.randint(0, 99) / 100)

    if not location:
        location_map = {"1": "Living Room", "2": "Bedroom", "3": "Kitchen"}
        location = location_map.get(sensor_id, "Unknown")

    if not sensor_id:
        sensor_map = {"Living Room": "1", "Bedroom": "2", "Kitchen": "3"}
        sensor_id = sensor_map.get(location, "0")

    return TemperatureData(
        value=round(value, 2),
        unit="°C",
        timestamp=datetime.now(),
        location=location,
        status="active",
        sensor_id=sensor_id,
        sensor_type="temperature",
        description=f"Temperature sensor in {location}"
    )


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/temperature", response_model=TemperatureData)
def get_temperature_by_location(location: str = Query(...)):
    if not location:
        raise HTTPException(status_code=400, detail="Location is required")
    return generate_temperature_data(location, "")


@app.get("/temperature/{sensor_id}", response_model=TemperatureData)
def get_temperature_by_id(sensor_id: str = Path(...)):
    if not sensor_id:
        raise HTTPException(status_code=400, detail="Sensor ID is required")
    return generate_temperature_data("", sensor_id)
