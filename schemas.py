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
    customerId: int
    carrierId: int
    dateCreated: datetime
    lastUpdate: datetime

    class Config:
        orm_mode = True

class _CustomerBase(_pydantic.BaseModel):
    firstName: str
    lastName: str
    address: str
    email: _pydantic.EmailStr

class _Login(_pydantic.BaseModel):
    email: _pydantic.EmailStr
    password: str
    role: str
class CustomerCreate(_CustomerBase):
    password: str

class Customer(_CustomerBase):
    id: Optional[int]
    deliveries: List[Delivery] = []
    dateCreated: datetime
    lastUpdate: datetime

    class Config:
        orm_mode = True

class _CarrierBase(_pydantic.BaseModel):
    firstName: str
    lastName: str
    address: str
    email: _pydantic.EmailStr

class CarrierCreate(_CarrierBase):
    password: str

class Carrier(_CarrierBase):
    id: Optional[int]
    deliveries: List[Delivery] = []
    dateCreated: datetime
    lastUpdate: datetime

    class Config:
        orm_mode = True