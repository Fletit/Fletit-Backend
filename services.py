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


def get_customer(db: _orm.Session, customer_id: int):
    return db.query(_models.Customer).filter(_models.Customer.id == customer_id).first()


def get_customer_by_email(db: _orm.Session, email: str):
    return db.query(_models.Customer).filter(_models.Customer.email == email).first()


def get_customers(db: _orm.Session, skip: int = 0, limit: int = 100):
    return db.query(_models.Customer).offset(skip).limit(limit).all()


def create_customer(db: _orm.Session, customer: _schemas.CustomerCreate):
    db_customer = _models.Customer(**customer.dict(), role="CUSTOMER")
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def get_carrier(db: _orm.Session, carrier_id: int):
    return db.query(_models.Carrier).filter(_models.Carrier.id == carrier_id).first()


def get_carrier_by_email(db: _orm.Session, email: str):
    return db.query(_models.Carrier).filter(_models.Carrier.email == email).first()


def get_carriers(db: _orm.Session, skip: int = 0, limit: int = 100):
    return db.query(_models.Carrier).offset(skip).limit(limit).all()


def create_carrier(db: _orm.Session, carrier: _schemas.CarrierCreate):
    db_carrier = _models.Carrier(**carrier.dict(), role="CARRIER")
    db.add(db_carrier)
    db.commit()
    db.refresh(db_carrier)
    return db_carrier

def update_carrier(db: _orm.Session, carrier_id: int, carrier: _schemas.Carrier):
    db_carrier = get_carrier(db=db, carrier_id=carrier_id)
    db_carrier.carModel = carrier.carModel
    db_carrier.carPlate = carrier.carPlate
    db_carrier.carrierType = carrier.carrierType
    db.commit()
    db.refresh(db_carrier)
    return db_carrier


def get_deliveries(db: _orm.Session, skip: int = 0, limit: int = 10):
    return db.query(_models.Delivery).offset(skip).limit(limit).all()


def create_delivery(db: _orm.Session, delivery: _schemas.DeliveryCreate, customer_id: int, carrier_id: int):
    delivery = _models.Delivery(**delivery.dict(), customerId=customer_id, carrierId = carrier_id)
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