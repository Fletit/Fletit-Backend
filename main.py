from typing import List
import fastapi as _fastapi
import sqlalchemy.orm as _orm
import services as _services
import schemas as _schemas

app = _fastapi.FastAPI()

_services.create_database()


@app.post("/users/", response_model=_schemas.User)
def create_user(user: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_user = _services.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise _fastapi.HTTPException(
            status_code=400, detail="woops the email is in use"
        )
    return _services.create_user(db=db, user=user)

@app.get("/users/", response_model=List[_schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    users = _services.get_users(db=db, skip=skip, limit=limit)
    return users

@app.post("/couriers/", response_model=_schemas.Courier)
def create_courier(courier: _schemas.CourierCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_courier = _services.get_courier_by_email(db=db, email=courier.email)
    if db_courier:
        raise _fastapi.HTTPException(
            status_code=400, detail="woops the email is in use"
        )
    return _services.create_courier(db=db, courier=courier)

@app.get("/couriers/", response_model=List[_schemas.Courier])
def read_couriers(skip: int = 0, limit: int = 10, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    couriers = _services.get_couriers(db=db, skip=skip, limit=limit)
    return couriers


@app.get("/users/{user_id}", response_model=_schemas.User)
def read_user(user_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_user = _services.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this user does not exist"
        )
    return db_user

@app.get("/couriers/{courier_id}", response_model=_schemas.Courier)
def read_courier(courier_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_courier = _services.get_courier(db=db, courier_id=courier_id)
    if db_courier is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this courier does not exist"
        )
    return db_courier


@app.post("/deliveries/", response_model=_schemas.Delivery)
def create_delivery(user_id: int, courier_id: int, delivery: _schemas.DeliveryCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_user = _services.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this user does not exist"
        )
    db_courier = _services.get_courier(db=db, courier_id=courier_id)
    if db_courier is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this courier does not exist"
        )    
    return _services.create_delivery(db=db, delivery=delivery, user_id=user_id, courier_id=courier_id)


@app.get("/deliveries/", response_model=List[_schemas.Delivery])
def read_deliveries(skip: int = 0, limit: int = 10, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    deliveries = _services.get_deliveries(db=db, skip=skip, limit=limit)
    return deliveries


@app.get("/deliveries/{delivery_id}", response_model=_schemas.Delivery)
def read_delivery(delivery_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    delivery = _services.get_delivery(db=db, delivery_id=delivery_id)
    if delivery is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this delivery does not exist"
        )

    return delivery


@app.delete("/deliveries/{delivery_id}")
def delete_delivery(delivery_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    _services.delete_delivery(db=db, delivery_id=delivery_id)
    return {"message": f"successfully deleted delivery with id: {delivery_id}"}


@app.put("/deliveries/{delivery_id}", response_model=_schemas.Delivery)
def update_delivery(delivery_id: int, delivery: _schemas.DeliveryCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return _services.update_delivery(db=db, delivery=delivery, delivery_id=delivery_id)
