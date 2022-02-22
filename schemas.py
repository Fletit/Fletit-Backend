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

class _NormalProductBase(_pydantic.BaseModel):
    height: str
    width: str
    large: str
    weight: str
    isFragile: str
    images: str

class NormalProductCreate(_NormalProductBase):
    pass
class NormalProduct(_NormalProductBase):
    id: Optional[int]
    dateCreated: datetime
    lastUpdate: datetime
    class Config:
        orm_mode = True
class _AnimalProductBase(_pydantic.BaseModel):
    age: str
    animalType: str
    breed: str
    name: str
    weight: str
    images: str
class AnimalProductCreate(_AnimalProductBase):
    pass
class AnimalProduct(_AnimalProductBase):
    id: Optional[int]
    dateCreated: datetime
    lastUpdate: datetime
    class Config:
        orm_mode = True

class _MotoProductBase(_pydantic.BaseModel):
    height: str
    width: str
    large: str
    weight: str
    isFragile: str
    images: str
class MotoProductCreate(_MotoProductBase):
    pass
class MotoProduct(_MotoProductBase):
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
    normalProducts: Optional[List[NormalProduct]] = []
    animalProducts: Optional[List[AnimalProduct]] = []
    motoProducts: Optional[List[MotoProduct]] = []
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