from typing import List, Optional
from datetime import datetime, date
import pydantic as _pydantic

class _CommentBase(_pydantic.BaseModel):
    message: str
    rating: float

class CommentCreate(_CommentBase):
    pass

class Comment(_CommentBase):
    id: Optional[int]
    customerId: int
    carrierId: int
    dateCreated: datetime
    lastUpdate: datetime

    class Config:
        orm_mode = True
class _ProductBase(_pydantic.BaseModel):
    height: str
    width: str
    large: str
    weight: str
    isFragile: bool
class ProductCreate(_ProductBase):
    pass

class Product(_ProductBase):
    id: Optional[int]
    deliveryId: int
    image: str
    dateCreated: datetime
    lastUpdate: datetime

    class Config:
        orm_mode = True
class _DeliveryBase(_pydantic.BaseModel):
    customerId: int
    originAddress: str
    destinationAddress: str
    state: str
    deliveryType: str
    deliveryDate: datetime

class DeliveryCreate(_DeliveryBase):
    pass

class Delivery(_DeliveryBase):
    id: Optional[int]
    carrierId: Optional[int]
    price: Optional[float]
    products: List[Product] = []
    dateCreated: datetime
    lastUpdate: datetime

    class Config:
        orm_mode = True

class _CustomerBase(_pydantic.BaseModel):
    firstName: str
    lastName: str
    birthdate: date
    email: _pydantic.EmailStr

class _Login(_pydantic.BaseModel):
    email: _pydantic.EmailStr
    password: str
    role: str
class CustomerCreate(_CustomerBase):
    password: str

class Customer(_CustomerBase):
    id: Optional[int]
    address: Optional[str]
    profilePic: Optional[str]
    deliveries: List[Delivery] = []
    comments: List[Comment] = []
    dateCreated: datetime
    lastUpdate: datetime

    class Config:
        orm_mode = True

class _CarrierBase(_pydantic.BaseModel):
    firstName: str
    lastName: str
    birthdate: date
    email: _pydantic.EmailStr

class CarrierCreate(_CarrierBase):
    password: str

class Carrier(_CarrierBase):
    id: Optional[int]
    address: Optional[str]
    profilePic: Optional[str]
    carModel: str
    carPlate: str
    carrierType: str
    helpers: int
    rating: float
    deliveries: List[Delivery] = []
    comments: List[Comment] = []
    dateCreated: datetime
    lastUpdate: datetime

    class Config:
        orm_mode = True