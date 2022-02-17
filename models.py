import datetime as _dt
import sqlalchemy as _sql
import sqlalchemy.orm as _orm

import database as _database

class Offer(_database.Base):
    __tablename__ = "offers"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    carrierId = _sql.Column(_sql.Integer, _sql.ForeignKey("carriers.id"))
    deliveryId = _sql.Column(_sql.Integer, _sql.ForeignKey("deliveries.id"))
    price = _sql.Column(_sql.Float)
    dateCreated = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    lastUpdate = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)

    delivery = _orm.relationship("Delivery", back_populates="offers")
    carrier = _orm.relationship("Carrier", back_populates="offers")
class Delivery(_database.Base):
    __tablename__ = "deliveries"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    originAddress = _sql.Column(_sql.String)
    destinationAddress = _sql.Column(_sql.String)
    state = _sql.Column(_sql.String)
    price = _sql.Column(_sql.Float)
    deliveryType = _sql.Column(_sql.String)
    deliveryDate = _sql.Column(_sql.DateTime)
    customerId = _sql.Column(_sql.Integer, _sql.ForeignKey("customers.id"))
    carrierId = _sql.Column(_sql.Integer, _sql.ForeignKey("carriers.id"))
    dateCreated = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    lastUpdate = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)

    owner = _orm.relationship("Customer", back_populates="deliveries")
    carrier = _orm.relationship("Carrier", back_populates="deliveries")
    products = _orm.relationship("Product", cascade="all, delete-orphan", uselist=True, back_populates="delivery")
    offers = _orm.relationship("Offer", cascade="all, delete-orphan", uselist=True, back_populates="delivery")
    
class Product(_database.Base):
    __tablename__ = "products"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    deliveryId = _sql.Column(_sql.Integer, _sql.ForeignKey("deliveries.id"))
    height = _sql.Column(_sql.String)
    width = _sql.Column(_sql.String)
    large = _sql.Column(_sql.String)
    weight = _sql.Column(_sql.String)
    isFragile = _sql.Column(_sql.Boolean, default=False)
    image = _sql.Column(_sql.String)
    dateCreated = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    lastUpdate = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)

    delivery = _orm.relationship("Delivery", back_populates="products")
class Customer(_database.Base):
    __tablename__ = "customers"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    firstName = _sql.Column(_sql.String)
    lastName = _sql.Column(_sql.String)
    birthdate = _sql.Column(_sql.Date)
    email = _sql.Column(_sql.String, unique=True, index=True)
    address = _sql.Column(_sql.String)
    password = _sql.Column(_sql.String)
    role = _sql.Column(_sql.String)
    profilePic = _sql.Column(_sql.String)
    dateCreated = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    lastUpdate = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)

    deliveries = _orm.relationship("Delivery", uselist=True, back_populates="owner")
    comments = _orm.relationship("Comment", cascade="all, delete-orphan", uselist=True, back_populates="owner")
class Carrier(_database.Base):
    __tablename__ = "carriers"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    firstName = _sql.Column(_sql.String)
    lastName = _sql.Column(_sql.String)
    birthdate = _sql.Column(_sql.Date)
    email = _sql.Column(_sql.String, unique=True, index=True)
    address = _sql.Column(_sql.String)
    password = _sql.Column(_sql.String)
    role = _sql.Column(_sql.String)
    profilePic = _sql.Column(_sql.String)
    carModel = _sql.Column(_sql.String)
    carPlate = _sql.Column(_sql.String)
    carrierType = _sql.Column(_sql.String)
    helpers = _sql.Column(_sql.Integer)
    rating = _sql.Column(_sql.Float)
    dateCreated = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    lastUpdate = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)

    deliveries = _orm.relationship("Delivery", uselist=True, back_populates="carrier")
    comments = _orm.relationship("Comment", cascade="all, delete-orphan", uselist=True, back_populates="carrier")
    offers = _orm.relationship("Offer", cascade="all, delete-orphan", uselist=True, back_populates="carrier")
class Comment(_database.Base):
    __tablename__ = "comments"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    customerId = _sql.Column(_sql.Integer, _sql.ForeignKey("customers.id"))
    owner = _orm.relationship("Customer", back_populates="comments")
    carrierId = _sql.Column(_sql.Integer, _sql.ForeignKey("carriers.id"))
    carrier = _orm.relationship("Carrier", back_populates="comments")
    message = _sql.Column(_sql.String)
    rating = _sql.Column(_sql.Float)
    dateCreated = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    lastUpdate = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
