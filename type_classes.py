from pydantic import BaseModel

#typing for used car data
class UsedCar(BaseModel):
    id:int
    variantid:int
    bodytype:str
    city:str
    price:int
    fueltype:str
    mileage:str
    make:str
    model:str
    gear:str
    owner:str

#typing for car variant data
class CarVariant(BaseModel):
    variant_id: int
    engine_cc: int
    ground_clearance_mm: int
    mileage_kmpl: float
    drive_type: str
    seating: int
    power: float
    cylinders: int
    gearbox: str
    top_speed_kmph: float
    enc: str
    length_mm: int
    width_mm: int
    height_mm: int
