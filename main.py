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

@app.get("/carriers/{carrier_id}", response_model=_schemas.Carrier)
def read_carrier(carrier_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_carrier = _services.get_carrier(db=db, carrier_id=carrier_id)
    if db_carrier is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this carrier does not exist"
        )
    return db_carrier


@app.post("/deliveries/", dependencies=[_fastapi.Depends(_auth_bearer.JWTBearer())], response_model=_schemas.Delivery)
def create_delivery(customer_id: int, carrier_id: int, delivery: _schemas.DeliveryCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_customer = _services.get_customer(db=db, customer_id=customer_id)
    if db_customer is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this customer does not exist"
        )
    db_carrier = _services.get_carrier(db=db, carrier_id=carrier_id)
    if db_carrier is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this carrier does not exist"
        )    
    return _services.create_delivery(db=db, delivery=delivery, customer_id=customer_id, carrier_id=carrier_id)


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
def update_delivery(delivery_id: int, delivery: _schemas.DeliveryCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return _services.update_delivery(db=db, delivery=delivery, delivery_id=delivery_id)

@app.get("/auth/")
def authenticate_user(access_token: str = _fastapi.Header(...), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    try:
        payload = _auth_handler.decodeJWT(access_token)
        print(payload)
    except:
        payload = None
    if payload:
        db_customer = _services.get_customer_by_email(db=db, email=payload["user_id"])
        return {"access_token": access_token, "user": jsonable_encoder(db_customer)}
    else:
        raise _fastapi.HTTPException(status_code=403, detail="Invalid token or expired token.")