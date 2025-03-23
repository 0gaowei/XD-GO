from datetime import datetime
from backend import db


class User(db.Model):
    __tablename__ = 'user'
    userid = db.Column(db.String(64), primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.Enum('buyer', 'seller', 'admin'), nullable=False)
    shipping_address = db.Column(db.String(200))
    createtime = db.Column(db.DateTime, default=datetime.utcnow)
    updatetime = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Category(db.Model):
    __tablename__ = 'category'
    catid = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    createtime = db.Column(db.DateTime, default=datetime.utcnow)
    updatetime = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Product(db.Model):
    __tablename__ = 'product'
    proid = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    catid = db.Column(db.String(64), db.ForeignKey('category.catid'))
    image = db.Column(db.LargeBinary)
    createtime = db.Column(db.DateTime, default=datetime.utcnow)
    updatetime = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Cart(db.Model):
    __tablename__ = 'cart'
    carid = db.Column(db.String(64), primary_key=True)
    userid = db.Column(db.String(64), db.ForeignKey('user.userid'))
    createtime = db.Column(db.DateTime, default=datetime.utcnow)
    updatetime = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CartItem(db.Model):
    __tablename__ = 'cartitem'
    id = db.Column(db.Integer, primary_key=True)
    carid = db.Column(db.String(64), db.ForeignKey('cart.carid'))
    proid = db.Column(db.String(64), db.ForeignKey('product.proid'))
    quantity = db.Column(db.Integer, nullable=False)
    createtime = db.Column(db.DateTime, default=datetime.utcnow)
    updatetime = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Shop(db.Model):
    __tablename__ = 'shop'
    shopid = db.Column(db.String(64), primary_key=True)
    userid = db.Column(db.String(64), db.ForeignKey('user.userid'))
    shopname = db.Column(db.String(100), nullable=False)
    shopdesc = db.Column(db.Text)
    createtime = db.Column(db.DateTime, default=datetime.utcnow)
    updatetime = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Order(db.Model):
    __tablename__ = 'order'
    orderid = db.Column(db.String(64), primary_key=True)
    userid = db.Column(db.String(64), db.ForeignKey('user.userid'))
    shopid = db.Column(db.String(64), db.ForeignKey('shop.shopid'))
    status = db.Column(db.Enum('pending', 'shipped', 'delivered'), default='pending')
    createtime = db.Column(db.DateTime, default=datetime.utcnow)
    updatetime = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class OrderItem(db.Model):
    __tablename__ = 'orderitem'
    id = db.Column(db.Integer, primary_key=True)
    orderid = db.Column(db.String(64), db.ForeignKey('order.orderid'))
    proid = db.Column(db.String(64), db.ForeignKey('product.proid'))
    productname = db.Column(db.String(100))
    price = db.Column(db.Numeric(10, 2))
    quantity = db.Column(db.Integer, nullable=False)
    createtime = db.Column(db.DateTime, default=datetime.utcnow)
    updatetime = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
