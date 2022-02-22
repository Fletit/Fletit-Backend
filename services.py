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

def update_customer(db: _orm.Session, customer: _schemas.Customer, db_customer: _schemas.Customer):
    for var, value in vars(customer).items():
        setattr(db_customer, var, value) if value else None
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

def update_carrier(db: _orm.Session, carrier: _schemas.Carrier, db_carrier: _schemas.Carrier):
    for var, value in vars(carrier).items():
        setattr(db_carrier, var, value) if value else None
    db.commit()
    db.refresh(db_carrier)
    return db_carrier


def get_deliveries(db: _orm.Session, skip: int = 0, limit: int = 10):
    return db.query(_models.Delivery).offset(skip).limit(limit).all()


def create_delivery(db: _orm.Session, delivery: _schemas.DeliveryCreate):
    normalProducts = []
    for normalProduct in delivery.normalProducts:
        product = _models.NormalProduct(**normalProduct.dict())
        normalProducts.append(product)
    animalProducts = []
    for animalProduct in delivery.animalProducts:
        product = _models.AnimalProduct(**animalProduct.dict())
        animalProducts.append(product)    
    motoProducts = []
    for motoProduct in delivery.motoProducts:
        product = _models.MotoProduct(**motoProduct.dict())
        motoProducts.append(product)    
    delivery = _models.Delivery(originAddress=delivery.originAddress, destinationAddress=delivery.destinationAddress, customerId=delivery.customerId, 
    state=delivery.state, deliveryType=delivery.deliveryType, deliveryDate=delivery.deliveryDate, normalProducts=normalProducts, 
    animalProducts=animalProducts, motoProducts=motoProducts)
    db.add(delivery)
    db.commit()
    db.refresh(delivery)
    return delivery


def get_delivery(db: _orm.Session, delivery_id: int):
    return db.query(_models.Delivery).filter(_models.Delivery.id == delivery_id).first()

def get_delivery_by_customer_id(db: _orm.Session, customer_id: int):
    return db.query(_models.Delivery).filter(_models.Delivery.customerId == customer_id).all()

def get_delivery_by_carrier_id(db: _orm.Session, carrier_id: int):
    return db.query(_models.Delivery).filter(_models.Delivery.carrierId == carrier_id).all()

def delete_delivery(db: _orm.Session, delivery_id: int):
    db.query(_models.Delivery).filter(_models.Delivery.id == delivery_id).delete()
    db.commit()


def update_delivery(db: _orm.Session, delivery: _schemas.Delivery, db_delivery: _schemas.Delivery):
    for var, value in vars(delivery).items():
        setattr(db_delivery, var, value) if value else None
    db.commit()
    db.refresh(db_delivery)
    return db_delivery

def get_offers(db: _orm.Session, skip: int = 0, limit: int = 10):
    return db.query(_models.Offer).offset(skip).limit(limit).all()

def create_offer(db: _orm.Session, offer: _schemas.OfferCreate):
    offer = _models.Offer(**offer.dict())
    db.add(offer)
    db.commit()
    db.refresh(offer)
    return offer

def get_offer(db: _orm.Session, offer_id: int):
    return db.query(_models.Offer).filter(_models.Offer.id == offer_id).first()

def delete_offer(db: _orm.Session, offer_id: int):
    db.query(_models.Offer).filter(_models.Offer.id == offer_id).delete()
    db.commit()