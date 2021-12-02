import sqlalchemy.orm as _orm

import models as _models, schemas as _schemas, database as _database


def create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user(db: _orm.Session, user_id: int):
    return db.query(_models.User).filter(_models.User.id == user_id).first()


def get_user_by_email(db: _orm.Session, email: str):
    return db.query(_models.User).filter(_models.User.email == email).first()


def get_users(db: _orm.Session, skip: int = 0, limit: int = 100):
    return db.query(_models.User).offset(skip).limit(limit).all()


def create_user(db: _orm.Session, user: _schemas.UserCreate):
    fake_hashed_password = user.password + "thisisnotsecure"
    db_user = _models.User(firstName=user.firstName, lastName=user.lastName, address=user.address, email=user.email, hashedPassword=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_courier(db: _orm.Session, courier_id: int):
    return db.query(_models.Courier).filter(_models.Courier.id == courier_id).first()


def get_courier_by_email(db: _orm.Session, email: str):
    return db.query(_models.Courier).filter(_models.Courier.email == email).first()


def get_couriers(db: _orm.Session, skip: int = 0, limit: int = 100):
    return db.query(_models.Courier).offset(skip).limit(limit).all()


def create_courier(db: _orm.Session, courier: _schemas.CourierCreate):
    fake_hashed_password = courier.password + "thisisnotsecure"
    db_courier = _models.Courier(firstName=courier.firstName, lastName=courier.lastName, address=courier.address, email=courier.email, hashedPassword=fake_hashed_password)
    db.add(db_courier)
    db.commit()
    db.refresh(db_courier)
    return db_courier


def get_deliveries(db: _orm.Session, skip: int = 0, limit: int = 10):
    return db.query(_models.Delivery).offset(skip).limit(limit).all()


def create_delivery(db: _orm.Session, delivery: _schemas.DeliveryCreate, user_id: int, courier_id: int):
    delivery = _models.Delivery(**delivery.dict(), userId=user_id, courierId = courier_id)
    db.add(delivery)
    db.commit()
    db.refresh(delivery)
    return delivery


def get_delivery(db: _orm.Session, delivery_id: int):
    return db.query(_models.Delivery).filter(_models.Delivery.id == delivery_id).first()


def delete_post(db: _orm.Session, delivery_id: int):
    db.query(_models.Delivery).filter(_models.Delivery.id == delivery_id).delete()
    db.commit()


def update_delivery(db: _orm.Session, delivery_id: int, delivery: _schemas.DeliveryCreate):
    db_delivery = get_delivery(db=db, delivery_id=delivery_id)
    db_delivery.state = delivery.state
    db_delivery.price = delivery.price
    db.commit()
    db.refresh(db_delivery)
    return db_delivery