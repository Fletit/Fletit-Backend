from typing import List, Optional
from datetime import datetime, date
import pydantic as _pydantic

class _CommentBase(_pydantic.BaseModel):
    message: str
    rating: float
    customerId: int
    carrierId: int
class CommentCreate(_CommentBase):
    pass
class Comment(_CommentBase):
    id: Optional[int]
    dateCreated: datetime
    lastUpdate: datetime

    class Config:
        orm_mode = True
class _OfferBase(_pydantic.BaseModel):
    deliveryId: int
    carrierId: int
    price: float
class OfferCreate(_OfferBase):
    pass
class Offer(_OfferBase):
    id: Optional[int]
    dateCreated: datetime
    lastUpdate: datetime

    class Config:
        orm_mode = True

class _ProductBase(_pydantic.BaseModel):
    productType: Optional[str]
    height: Optional[str]
    width: Optional[str]
    large: Optional[str]
    age: Optional[str]
    animalType: Optional[str]
    breed: Optional[str]
    name: Optional[str]
    weight: Optional[str]
    isFragile: Optional[str]
    images: str

class ProductCreate(_ProductBase):
    pass
class Product(_ProductBase):
    id: Optional[int]
    dateCreated: datetime
    lastUpdate: datetime
    class Config:
        orm_mode = True

class _DeliveryBase(_pydantic.BaseModel):
    customerId: int
    originAddress: str
    destinationAddress: str
    state: str
    products: List[Product] = []
    deliveryType: str
    deliveryDate: datetime

class DeliveryCreate(_DeliveryBase):
    pass

class Delivery(_DeliveryBase):
    id: Optional[int]
    carrierId: Optional[int]
    price: Optional[float]
    offers: List[Offer] = []
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
    cellphone: Optional[str]
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
    cellphone: Optional[str]
    profilePic: Optional[str]
    carModel: Optional[str]
    carPlate: Optional[str]
    carrierType: Optional[str]
    helpers: Optional[int]
    rating: Optional[float]
    deliveries: List[Delivery] = []
    comments: List[Comment] = []
    offers: List[Offer] = []
    dateCreated: datetime
    lastUpdate: datetime

    class Config:
        orm_mode = True