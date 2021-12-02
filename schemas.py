from typing import List, Optional
from datetime import datetime
import pydantic as _pydantic


class _DeliveryBase(_pydantic.BaseModel):
    originAddress: str
    destinationAddress: str
    state: str = "Started"
    price: float

class DeliveryCreate(_DeliveryBase):
    pass

class Delivery(_DeliveryBase):
    id: Optional[int]
    userId: int
    courierId: int
    dateCreated: datetime
    lastUpdate: datetime

    class Config:
        orm_mode = True

class _UserBase(_pydantic.BaseModel):
    firstName: str
    lastName: str
    address: str
    email: str

class UserCreate(_UserBase):
    password: str

class User(_UserBase):
    id: Optional[int]
    deliveries: List[Delivery] = []
    dateCreated: datetime
    lastUpdate: datetime

    class Config:
        orm_mode = True

class _CourierBase(_pydantic.BaseModel):
    firstName: str
    lastName: str
    address: str
    email: str

class CourierCreate(_CourierBase):
    password: str

class Courier(_CourierBase):
    id: Optional[int]
    deliveries: List[Delivery] = []
    dateCreated: datetime
    lastUpdate: datetime

    class Config:
        orm_mode = True