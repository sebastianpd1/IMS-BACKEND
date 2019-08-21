from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()



class Products(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    purchases = db.relationship("Transactions", back_populates="products")


    def serialize(self):
        return {
            "id":self.id,
            "item": self.item,
            "description": self.description,
            "quantity": self.quantity
        }

class Purchases(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.Date, default=datetime.datetime.now())
    products = db.relationship("Transactions", back_populates="purchases")



    def serialize(self):
        return {
            "id":self.id,
            "date": self.created_at,
        }

class Sales(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.Date, default=datetime.datetime.now())

    def serialize(self):
        return {
            "id":self.id,
            "date": self.created_at,
        }

#class Transactions(db.Model):
#id = db.Column(db.Integer, primary_key=True)

class Transactions(db.Model):

    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    purchases_id = db.Column(db.Integer, db.ForeignKey('purchases.id'), primary_key=True)
    products_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    purchases = db.relationship("Purchases", back_populates="products")
    products = db.relationship("Products", back_populates="purchases")
    quantity = db.Column(db.Integer, nullable=False)

    def serialize(self):
        return {
            "id":self.id,
            "item": self.item,
            "description": self.description,
            "quantity": self.quantity
        }

    def sum(self, id):
        t = list(map(lambda x: x.serialize(), Transactions.query_all()))
        t = list(filter(lambda x: x.purchases_id == id, t))

        total = 0
        for e in t:
            total += int(e.quantity)

        return total

    #  def __init__(self, products, quantity):

    #     self.products = products
    #     self.quantity = quantity

    # @hybrid_property
    # def length(self):
    #     x= Products.query.all()
    #     x =list x.serialize
    #     x.map
    #     yertyer
    #     t
    #     return total