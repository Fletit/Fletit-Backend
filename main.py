from typing import List
import fastapi as _fastapi
import sqlalchemy.orm as _orm
import services as _services
import schemas as _schemas
import auth_handler as _auth_handler
import auth_bearer as _auth_bearer
from fastapi.encoders import jsonable_encoder

app = _fastapi.FastAPI()

_services.create_database()

@app.post("/customers/")
async def create_customer(customer: _schemas.CustomerCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_customer = _services.get_customer_by_email(db=db, email=customer.email)
    if db_customer:
        raise _fastapi.HTTPException(
            status_code=400, detail="woops the email is in use"
        )
    db_customer = _services.create_customer(db=db, customer=customer)
    return _auth_handler.signJWT(customer.email, jsonable_encoder(db_customer))

@app.post("/login/")
async def login(user: _schemas._Login, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_user = None
    if (user.role.lower() == "customer"):
        db_user = _services.get_customer_by_email(db=db, email=user.email)
    else:
        db_user = _services.get_carrier_by_email(db=db, email=user.email)

    if db_user and db_user.password == user.password:
        return _auth_handler.signJWT(user.email, jsonable_encoder(db_user))
    else:
        raise _fastapi.HTTPException(
            status_code=400, detail="woops wrong login details!"
        )

@app.get("/customers/", response_model=List[_schemas.Customer])
def read_customers(skip: int = 0, limit: int = 10, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    customers = _services.get_customers(db=db, skip=skip, limit=limit)
    return customers

@app.post("/carriers/")
def create_carrier(carrier: _schemas.CarrierCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_carrier = _services.get_carrier_by_email(db=db, email=carrier.email)
    if db_carrier:
        raise _fastapi.HTTPException(
            status_code=400, detail="woops the email is in use"
        )
    db_carrier = _services.create_carrier(db=db, carrier=carrier)
    return _auth_handler.signJWT(carrier.email, jsonable_encoder(db_carrier))

@app.get("/carriers/", response_model=List[_schemas.Carrier])
def read_carriers(skip: int = 0, limit: int = 10, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    carriers = _services.get_carriers(db=db, skip=skip, limit=limit)
    return carriers


@app.get("/customers/{customer_id}", response_model=_schemas.Customer)
def read_customer(customer_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_customer = _services.get_customer(db=db, customer_id=customer_id)
    if db_customer is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this customer does not exist"
        )
    return db_customer

@app.put("/customers/{customer_id}", response_model=_schemas.Customer)
def update_customer(customer_id: int, customer: _schemas.Customer, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_customer = _services.get_customer(db=db, customer_id=customer_id)
    if db_customer is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this customer does not exist"
        )
    return _services.update_customer(db=db, customer=customer, db_customer=db_customer)

@app.get("/carriers/{carrier_id}", response_model=_schemas.Carrier)
def read_carrier(carrier_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_carrier = _services.get_carrier(db=db, carrier_id=carrier_id)
    if db_carrier is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this carrier does not exist"
        )
    return db_carrier

@app.put("/carriers/{carrier_id}", response_model=_schemas.Carrier)
def update_carrier(carrier_id: int, carrier: _schemas.Carrier, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_carrier = _services.get_carrier(db=db, carrier_id=carrier_id)
    if db_carrier is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this carrier does not exist"
        )
    return _services.update_carrier(db=db, carrier=carrier, db_carrier=db_carrier)

@app.post("/deliveries/", dependencies=[_fastapi.Depends(_auth_bearer.JWTBearer())], response_model=_schemas.Delivery)
def create_delivery(delivery: _schemas.DeliveryCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_customer = _services.get_customer(db=db, customer_id=delivery.customerId)
    if db_customer is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this customer does not exist"
        ) 
    return _services.create_delivery(db=db, delivery=delivery)


@app.get("/deliveries/", dependencies=[_fastapi.Depends(_auth_bearer.JWTBearer())], response_model=List[_schemas.Delivery])
def read_deliveries(skip: int = 0, limit: int = 10, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    deliveries = _services.get_deliveries(db=db, skip=skip, limit=limit)
    return deliveries


@app.get("/deliveries/{delivery_id}", dependencies=[_fastapi.Depends(_auth_bearer.JWTBearer())], response_model=_schemas.Delivery)
def read_delivery(delivery_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    delivery = _services.get_delivery(db=db, delivery_id=delivery_id)
    if delivery is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this delivery does not exist"
        )

    return delivery


@app.delete("/deliveries/{delivery_id}", dependencies=[_fastapi.Depends(_auth_bearer.JWTBearer())])
def delete_delivery(delivery_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    _services.delete_delivery(db=db, delivery_id=delivery_id)
    return {"message": f"successfully deleted delivery with id: {delivery_id}"}


@app.put("/deliveries/{delivery_id}", dependencies=[_fastapi.Depends(_auth_bearer.JWTBearer())], response_model=_schemas.Delivery)
def update_delivery(delivery_id: int, delivery: _schemas.Delivery, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_delivery = _services.get_delivery(db=db, delivery_id=delivery_id)
    if db_delivery is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this delivery does not exist"
        )
    return _services.update_delivery(db=db, delivery=delivery, db_delivery=db_delivery)

@app.get("/auth/")
def authenticate_user(access_token: str = _fastapi.Header(...), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    try:
        payload = _auth_handler.decodeJWT(access_token)
    except:
        payload = None
    if payload:
        db_user = _services.get_customer_by_email(db=db, email=payload["user_id"])
        if db_user:
            return {"access_token": access_token, "user": jsonable_encoder(db_user)}
        else:
            db_user = _services.get_carrier_by_email(db=db, email=payload["user_id"])
            return {"access_token": access_token, "user": jsonable_encoder(db_user)}
    else:
        raise _fastapi.HTTPException(status_code=403, detail="Invalid token or expired token.")

@app.get("/getDeliveriesByCustomerId", dependencies=[_fastapi.Depends(_auth_bearer.JWTBearer())], response_model=List[_schemas.Delivery])
def get_deliveries_by_customer_id(customer_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    deliveries = _services.get_delivery_by_customer_id(db=db, customer_id=customer_id)
    return deliveries

@app.get("/getDeliveriesByCarrierId", dependencies=[_fastapi.Depends(_auth_bearer.JWTBearer())], response_model=List[_schemas.Delivery])
def get_deliveries_by_carrier_id(carrier_id: int, delivery_type: str, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    deliveries = _services.get_delivery_by_carrier_id(db=db, carrier_id=carrier_id, delivery_type=delivery_type)
    return deliveries

@app.post("/offers/", dependencies=[_fastapi.Depends(_auth_bearer.JWTBearer())], response_model=_schemas.Offer)
def create_offer(offer: _schemas.OfferCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_carrier = _services.get_carrier(db=db, carrier_id=offer.carrierId)
    if db_carrier is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this carrier does not exist"
        )
    db_delivery = _services.get_delivery(db=db, delivery_id=offer.deliveryId)
    if db_delivery is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this delivery does not exist"
        ) 
    return _services.create_offer(db=db, offer=offer)

@app.delete("/offers/{offer_id}", dependencies=[_fastapi.Depends(_auth_bearer.JWTBearer())])
def delete_offer(offer_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    _services.delete_offer(db=db, offer_id=offer_id)
    return {"message": f"successfully deleted offer with id: {offer_id}"}

@app.get("/offers/{offer_id}", dependencies=[_fastapi.Depends(_auth_bearer.JWTBearer())], response_model=_schemas.Offer)
def read_offer(offer_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    offer = _services.get_offer(db=db, offer_id=offer_id)
    if offer is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this offer does not exist"
        )

    return offer

@app.post("/acceptOffer", dependencies=[_fastapi.Depends(_auth_bearer.JWTBearer())])
def accept_offer(offer_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    offer = _services.get_offer(db=db, offer_id=offer_id)
    if offer is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this offer does not exist"
        )
    db_delivery = _services.get_delivery(db=db, delivery_id=offer.deliveryId)
    if db_delivery is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this delivery does not exist"
        ) 
    updatedDelivery = db_delivery
    updatedDelivery.price = offer.price
    updatedDelivery.state = "ACCEPTED"
    updatedDelivery.carrierId = offer.carrierId
    return _services.update_delivery(db=db, delivery=updatedDelivery, db_delivery=db_delivery)

@app.post("/startDelivery", dependencies=[_fastapi.Depends(_auth_bearer.JWTBearer())])
def start_delivery(delivery_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_delivery = _services.get_delivery(db=db, delivery_id=delivery_id)
    if db_delivery is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this delivery does not exist"
        ) 
    updatedDelivery = db_delivery
    updatedDelivery.state = "STARTED"
    return _services.update_delivery(db=db, delivery=updatedDelivery, db_delivery=db_delivery)

@app.post("/incommingDelivery", dependencies=[_fastapi.Depends(_auth_bearer.JWTBearer())])
def incomming_delivery(delivery_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_delivery = _services.get_delivery(db=db, delivery_id=delivery_id)
    if db_delivery is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this delivery does not exist"
        ) 
    updatedDelivery = db_delivery
    updatedDelivery.state = "INCOMMING"
    return _services.update_delivery(db=db, delivery=updatedDelivery, db_delivery=db_delivery)

@app.post("/arrivedDelivery", dependencies=[_fastapi.Depends(_auth_bearer.JWTBearer())])
def finish_delivery(delivery_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_delivery = _services.get_delivery(db=db, delivery_id=delivery_id)
    if db_delivery is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this delivery does not exist"
        ) 
    updatedDelivery = db_delivery
    updatedDelivery.state = "ARRIVED"
    return _services.update_delivery(db=db, delivery=updatedDelivery, db_delivery=db_delivery)

@app.post("/finishDelivery", dependencies=[_fastapi.Depends(_auth_bearer.JWTBearer())])
def finish_delivery(delivery_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_delivery = _services.get_delivery(db=db, delivery_id=delivery_id)
    if db_delivery is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this delivery does not exist"
        ) 
    updatedDelivery = db_delivery
    updatedDelivery.state = "FINISHED"
    return _services.update_delivery(db=db, delivery=updatedDelivery, db_delivery=db_delivery)

@app.post("/comments/", dependencies=[_fastapi.Depends(_auth_bearer.JWTBearer())], response_model=_schemas.Comment)
def create_comment(comment: _schemas.CommentCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_carrier = _services.get_carrier(db=db, carrier_id=comment.carrierId)
    if db_carrier is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this carrier does not exist"
        )
    _services.create_comment(db=db, comment=comment)
    _services.update_carrier_rating(db=db, carrier_id=comment.carrierId)

@app.delete("/comments/{comment_id}", dependencies=[_fastapi.Depends(_auth_bearer.JWTBearer())])
def delete_comment(comment_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    _services.delete_comment(db=db, comment_id=comment_id)
    return {"message": f"successfully deleted comment with id: {comment_id}"}

@app.get("/comments/{comment_id}", dependencies=[_fastapi.Depends(_auth_bearer.JWTBearer())], response_model=_schemas.Comment)
def read_comment(comment_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    comment = _services.get_comment(db=db, comment_id=comment_id)
    if comment is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this comment does not exist"
        )

    return comment