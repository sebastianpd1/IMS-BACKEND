from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
import datetime

db = SQLAlchemy()



class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer, nullable=True)
    #ACA ABAJO ESTAN MIS RELACIONES CON LAS DEMAS TABLAS
    purchases = db.relationship("Transactions", back_populates="products")

    def serialize(self):
        return {
            "id":self.id,
            "item": self.item,
            "description": self.description,
            "quantity": self.quantity,
            #ACA ABAJO HAGO SERIALIZACION PARA LAS RELACIONES CON LAS DEMAS TABLAS
            "purchases": list(map(lambda x: x.serialize(), self.purchases)),
        }


class Purchases(db.Model):
    __tablename__ = 'purchases'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.Date, default=datetime.datetime.now())
    #ACA ABAJO ESTAN MIS RELACIONES CON LAS DEMAS TABLAS
    products = db.relationship("Transactions", back_populates="purchases")



    def serialize(self):
        return {
            "id":self.id,
            "date": self.created_at,
            #ACA ABAJO HAGO SERIALIZACION PARA LAS RELACIONES CON LAS DEMAS TABLAS
            "products": list(map(lambda x: x.serialize(), self.products)),
        }

class Sales(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.Date, default=datetime.datetime.now())

    def serialize(self):
        return {
            "id":self.id,
            "date": self.created_at,
        }

class Transactions(db.Model):

    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    purchases_id = db.Column(db.Integer, db.ForeignKey('purchases.id'), primary_key=True)
    products_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    #ACA ABAJO ESTAN MIS RELACIONES CON LAS DEMAS TABLAS
    products = db.relationship("Products", back_populates="purchases")
    purchases = db.relationship("Purchases", back_populates="products")

    def __init__(self, products_id, purchases_id, quantity):
        self.purchases_id = purchases_id
        self.products_id = products_id
        self.quantity = quantity

    def serialize(self):
        return {
            "id":self.id,
            "purchases_id": self.purchases_id,
            "products_id": self.products_id,
            "quantity": self.quantity,
        }

    @hybrid_method
    def purchasesTotal(self,products_id):
        t = list(map(lambda x: x.serialize(), Transactions.query.filter_by(purchases_id=products_id)))
        total = 0
        for e in t:
            total += int(e["quantity"])
        return str(total)

    # def sum(self, id):
    #     t = list(map(lambda x: x.serialize(), Transactions.query_all()))
    #     t = list(filter(lambda x: x.purchases_id == id, t))

    #     total = 0
    #     for e in t:
    #         total += int(e.quantity)

    #     return total

    #  def __init__(self, products, quantity):

    #     self.products = products
    #     self.quantity = quantity

