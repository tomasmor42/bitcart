# coding: utf-8
# from sqlalchemy import BigInteger, Boolean, CheckConstraint, Column, DateTime, ForeignKey, Integer, LargeBinary, Numeric, SmallInteger, String, Text, UniqueConstraint, text
# from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .db import db

# shortcuts
Model = db.Model
Column = db.Column
Integer = db.Integer
String = db.String
Boolean = db.Boolean
Numeric = db.Numeric
DateTime = db.DateTime
Text = db.Text
ForeignKey = db.ForeignKey


class User(Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, index=True)
    hashed_password = Column(String)
    is_superuser = Column(Boolean(), default=False)


class Wallet(Model):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=1000))
    xpub = Column(String(length=1000))
    balance = Column(Numeric(16, 8))
    user_id = Column(Integer, ForeignKey(User.id))
    user = relationship(User, backref="wallets")


class Store(Model):
    __tablename__ = 'stores'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(1000))
    domain = Column(String(1000))
    template = Column(String(1000))
    email = Column(String(1000))
    wallet_id = Column(
        ForeignKey(
            'wallets.id',
            deferrable=True,
            initially='DEFERRED'),
        nullable=False,
        index=True)
    email_host = Column(String(1000))
    email_password = Column(String(1000))
    email_port = Column(Integer)
    email_use_ssl = Column(Boolean)
    email_user = Column(String(1000))

    wallet = relationship('Wallet')


class Product(Model):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Numeric(16, 8), nullable=False)
    quantity = Column(Numeric(16, 8), nullable=False)
    title = Column(String(1000), nullable=False)
    date = Column(DateTime(True), nullable=False)
    description = Column(Text)
    image = Column(String(100))
    store_id = Column(
        ForeignKey(
            'stores.id',
            deferrable=True,
            initially='DEFERRED'),
        nullable=False,
        index=True)
    status = Column(String(1000), nullable=False)

    store = relationship('Store')


class ParentXChild(db.Model):
    __tablename__ = 'invoicesxproducts'

    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'))


class Invoice(Model):
    __tablename__ = 'invoices'

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Numeric(16, 8), nullable=False)
    status = Column(String(1000), nullable=False)
    date = Column(DateTime(True), nullable=False)
    bitcoin_address = Column(String(255), nullable=False)
    bitcoin_url = Column(String(255), nullable=False)
    products = relationship("Product", secondary=ParentXChild)

    @classmethod
    def parent(cls):
        return Product
