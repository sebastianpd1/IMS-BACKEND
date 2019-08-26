from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
import datetime

db = SQLAlchemy()

##########################################################################################################
############################################ PRODUCTS TABLE ##############################################
##########################################################################################################


class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer, nullable=True)
    #ACA ABAJO ESTAN MIS RELACIONES CON LAS DEMAS TABLAS
    purchases = db.relationship("Transactions", back_populates="products")
    sales = db.relationship("Transactions", back_populates="products")
    warehouses = db.relationship("Transactions", back_populates="products")

    def serialize(self):
        return {
            "id":self.id,
            "item": self.item,
            "description": self.description,
            "quantity": self.quantity,
            #ACA ABAJO HAGO SERIALIZACION PARA LAS RELACIONES CON LAS DEMAS TABLAS
            "transactions": list(map(lambda x: x.serialize(), self.purchases)),
        }


##########################################################################################################
############################################ PURCHASES TABLE ##############################################
##########################################################################################################


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
            "products": list(map(lambda x: x.serialize(), self.products))
        }

##########################################################################################################
############################################ SALES TABLE ##############################################
##########################################################################################################


class Sales(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    #ACA ABAJO ESTAN MIS RELACIONES CON LAS DEMAS TABLAS
    products = db.relationship("Transactions", back_populates="sales")

    def serialize(self):
        return {
            "id":self.id,
            "date": self.created_at,
            #ACA ABAJO HAGO SERIALIZACION PARA LAS RELACIONES CON LAS DEMAS TABLAS
            "products": list(map(lambda x: x.serialize(), self.products))
        }

##########################################################################################################
############################################ TRANSACTIONS TABLE ##############################################
##########################################################################################################

class Transactions(db.Model):

    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    purchases_id = db.Column(db.Integer, db.ForeignKey('purchases.id'), nullable=True)
    sales_id = db.Column(db.Integer, db.ForeignKey('sales.id'), nullable=True)
    warehouses_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'), nullable=True)
    products_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer, nullable=False)
    #ACA ABAJO ESTAN MIS RELACIONES CON LAS DEMAS TABLAS
    products = db.relationship("Products", back_populates="purchases")
    purchases = db.relationship("Purchases", back_populates="products")
    sales = db.relationship("Sales", back_populates="products")
    warehouses = db.relationship("Warehouses", back_populates="products")

    def __init__(self, products_id, purchases_id, sales_id, warehouses_id, quantity):
        self.purchases_id = purchases_id
        self.products_id = products_id
        self.sales_id = sales_id
        self.warehouses_id = warehouses_id
        self.quantity = quantity

    def serialize(self):
        return {
            "id":self.id,
            "products_id": self.products_id,
            "purchases_id": self.purchases_id,
            "warehouses_id": self.warehouses_id,
            "sales_id": self.sales_id,
            "quantity": self.quantity
        }

    @hybrid_method
    def purchasesTotal(self,products_id):
        t = list(map(lambda x: x.serialize(), Transactions.query.filter_by(purchases_id=products_id)))
        total = 0
        for e in t:
            total += int(e["quantity"])
        return str(total)

##########################################################################################################
############################################ WAREHOUSE TABLE #############################################
##########################################################################################################


class Warehouses(db.Model):
    __tablename__ = 'warehouses'
    id = db.Column(db.Integer, primary_key=True)
    warehouse_name = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(80), nullable=False)
    #ACA ABAJO ESTAN MIS RELACIONES CON LAS DEMAS TABLAS
    products = db.relationship("Transactions", back_populates="warehouses")

    def serialize(self):
        return {
            "id":self.id,
            "warehouse_name": self.warehouse_name,
            "location": self.location,
            #ACA ABAJO HAGO SERIALIZACION PARA LAS RELACIONES CON LAS DEMAS TABLAS
            "products": list(map(lambda x: x.serialize(), self.products))
        }