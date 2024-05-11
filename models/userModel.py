import datetime

from sqlalchemy import Integer, DateTime, String, Float, Column, ForeignKey
from sqlalchemy.orm import Relationship

from database import db


class User(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    email = Column(String(80), unique=True, nullable=False)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(80), nullable=False)
    orders = Relationship("Order", backref="user", lazy=True)


# Uocena je greska prilikom kreiranja baze!!

# Kada kreiramo sample imamo jedan element npr Feri
# Kada Zelimo da napravimo magacine gde mogu da se oni koriste dolazimo u cajtnot gde 1 magacin moze da ima samo 1 feri ne moze npr da ima presil!
# Poboljsanje ali me mrzi mislim da je narusena 4NF BojsCodova gde treba da imamo 2 tabelu koja ce da sadrzi id sample i kolicinu koju imaju na stanju
# mi samo Supplie treba da ima naziv lokaciju i magacin polje tj tabelu a tabela magacin listu sample id i kolicine!!!!

# sada je ovakao
# description = Column(String(80))
# state_on_supp = Column(Integer)
# location = Column(String(90))
# sample_id = Column(Integer, ForeignKey("sample.id"))

# Realno greska jer sample ne treba da bude poznat supplies nego samo magacinu

class Sample(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(80))
    description = Column(String(80))
    price = Column(Float)
    categories = Relationship("Category", backref="sample", lazy=True)
    magacines = Relationship("Magacin", backref="sample", lazy=True)
    order_items = Relationship("OrderItem", backref="sample", lazy=True)


class Category(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(80))
    description = Column(String(80))
    sample_id = Column(Integer, ForeignKey(Sample.id))


class Magacin(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    sample_id = Column(Integer, ForeignKey("sample.id"))
    amount = Column(Integer)
    supplies = Relationship("Supplie", backref="magacin", lazy=True)


class Supplie(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(80))
    description = Column(String(80))
    location = Column(String(90))
    magacin_id = Column(Integer, ForeignKey("magacin.id"))


class Status(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(80))
    orders = Relationship("Order", backref="status", lazy=True)


class Delivery(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    order = Relationship("Order", backref="delivery", uselist=False)
    expected_del = Column(DateTime)
    real_delivery = Column(DateTime)


class Order(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    date = Column(DateTime, default=datetime.datetime.now())
    user_id = Column(Integer, ForeignKey("user.id"))
    status_id = Column(Integer, ForeignKey("status.id"))
    items = Relationship("OrderItem", backref="order", lazy=True)
    delivery_id = Column(ForeignKey("delivery.id"))


class OrderItem(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    order_id = Column(Integer, ForeignKey("order.id"))
    sample_id = Column(Integer, ForeignKey("sample.id"))

    amount = Column(Float)


class ProductSales(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    product_id = Column(Integer)
    product_name = Column(String(30))
    quantity = Column(Integer)
    price = Column(Float)
    sale_date = Column(DateTime)
    customer_id = Column(Integer)
    customer_name = Column(String(30))
    region = Column(String(30))
