import datetime as _dt
import sqlalchemy as _sql
import sqlalchemy.orm as _orm

import database as _database


class Customer(_database.Base):
    __tablename__ = "customers"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    firstName = _sql.Column(_sql.String)
    lastName = _sql.Column(_sql.String)
    email = _sql.Column(_sql.String, unique=True, index=True)
    address = _sql.Column(_sql.String)
    hashedPassword = _sql.Column(_sql.String)
    dateCreated = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    lastUpdate = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)

    deliveries = _orm.relationship("Delivery", back_populates="owner")


class Delivery(_database.Base):
    __tablename__ = "deliveries"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    originAddress = _sql.Column(_sql.String)
    destinationAddress = _sql.Column(_sql.String)
    state = _sql.Column(_sql.String)
    price = _sql.Column(_sql.Float)
    customerId = _sql.Column(_sql.Integer, _sql.ForeignKey("customers.id"))
    carrierId = _sql.Column(_sql.Integer, _sql.ForeignKey("carriers.id"))
    dateCreated = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    lastUpdate = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)

    owner = _orm.relationship("Customer", back_populates="deliveries")
    carrier = _orm.relationship("Carrier", back_populates="deliveries")

class Carrier(_database.Base):
    __tablename__ = "carriers"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    firstName = _sql.Column(_sql.String)
    lastName = _sql.Column(_sql.String)
    email = _sql.Column(_sql.String, unique=True, index=True)
    address = _sql.Column(_sql.String)
    hashedPassword = _sql.Column(_sql.String)
    dateCreated = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    lastUpdate = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)

    deliveries = _orm.relationship("Delivery", back_populates="carrier")