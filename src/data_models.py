from pydantic import BaseModel

class Listing(BaseModel):
    listing_id: str
    listing_name: str
    model_name: str
    model_id: str
    make_name: str
    price: int
    mileage: int
    transmission: str
    fuel: str
