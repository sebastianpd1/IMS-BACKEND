import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from sqlalchemy import func
from utils import APIException, generate_sitemap, verify_json, verify_json_single
from models import db, Products, Purchases, Sales, Transactions, Warehouses
import json
from flask_jwt_simple import JWTManager, jwt_required, create_jwt, get_jwt_identity

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

##########################################################################################################
############################################ PRODUCTS TABLE ##############################################
##########################################################################################################

@app.route('/products/all', methods=['GET', 'POST'])

def productsAllGet():

    # POST request

    if request.method == 'POST':

        body = request.get_json()
        missing_item = verify_json_single(body,'item','description')
        if missing_item:
            raise APIException('You need to specify the ' + missing_item, status_code=400)
        products = Products(item=body['item'], description=body['description'], quantity=body['quantity'])
        db.session.add(products)
        db.session.commit()
        all_products = Products.query.filter().order_by(Products.item)
        all_products = list(map(lambda e: e.serialize(), all_products))
        return jsonify(all_products), 200

    # GET request

    if request.method == 'GET':

        all_products = Products.query.all()
        all_products = list(map(lambda e: e.serialize(), all_products))
        return jsonify(all_products), 200

    return "Invalid Method", 404

############################################ DELETE PRODUCTS ############################################

@app.route('/products/delete/<int:products_id>', methods=['DELETE'])

def productsDelete(products_id):

    if request.method == 'DELETE':
        products = Products.query.get(products_id)
        if products is None:
            raise APIException('Product not found', status_code=404)
        db.session.delete(products)
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404

##########################################################################################################
############################################ PURCHASES TABLE ##############################################
##########################################################################################################

############################################ GET ALL PURCHASES / CREATE NEW PURCHASE ############################################


@app.route('/purchases/all', methods=['GET', 'POST'])

def purchasesAllGet():

    # POST request

    if request.method == 'POST':

        body = request.get_json()
        purchases = Purchases()
        db.session.add(purchases)
        db.session.commit()
        all_purchases = Purchases.query.all()
        all_purchases = list(map(lambda e: e.serialize(), all_purchases))
        return jsonify(all_purchases), 200

    # GET request

    if request.method == 'GET':

        all_purchases = Purchases.query.all()
        all_purchases = list(map(lambda e: e.serialize(), all_purchases))
        return jsonify(all_purchases), 200

    return "Invalid Method", 404

############################################ DELETE PURCHASES ############################################

@app.route('/purchases/delete/<int:purchases_id>', methods=['DELETE'])

def purchasesDelete(purchases_id):

    if request.method == 'DELETE':
        purchases = Purchases.query.get(purchases_id)
        if purchases is None:
            raise APIException('Purchase not found', status_code=404)
        db.session.delete(purchases)
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404
##########################################################################################################
############################################ SALES TABLE ##############################################
##########################################################################################################

############################################ GET ALL SALES / CREATE NEW SALE ############################################


@app.route('/sales/all', methods=['GET', 'POST'])

def salesAllGet():

    # POST request

    if request.method == 'POST':

        body = request.get_json()
        sales = Sales()
        db.session.add(sales)
        db.session.commit()
        all_sales = Sales.query.all()
        all_sales = list(map(lambda e: e.serialize(), all_sales))
        return jsonify(all_sales), 200

    # GET request

    if request.method == 'GET':

        all_sales = Sales.query.all()
        all_sales = list(map(lambda e: e.serialize(), all_sales))
        return jsonify(all_sales), 200

    return "Invalid Method", 404

############################################ DELETE SALES ############################################

@app.route('/sales/delete/<int:sales_id>', methods=['DELETE'])

def salesDelete(sales_id):

    if request.method == 'DELETE':
        sales = Sales.query.get(sales_id)
        if sales is None:
            raise APIException('Sale not found', status_code=404)
        db.session.delete(sales)
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404


##########################################################################################################
############################################ TRANSACTIONS BETA TABLE ##############################################
##########################################################################################################

############################################ GET ALL / CREATE A NEW ONE TRANSACTIONS ############################################

@app.route('/transactions/new/map/', methods=['GET', 'POST'])

def transactionsNewPostbeta():

    # POST request

    if request.method == 'POST':

        body = request.get_json()
        missing_item = verify_json(body,'products_id','quantity','warehouses_id')
        if missing_item:
           raise APIException('You need to specify the ' + missing_item, status_code=400)
        if 'sales_id' in body[0]:
            purchases = Purchases()
            db.session.add(purchases)
            db.session.commit()
            purchases_id = purchases.id
            for e in body:
                e["purchases_id"]=purchases_id
        else:
            sales = Sales()
            db.session.add(sales)
            db.session.commit()
            sales_id = sales.id
            for e in body:
                e["sales_id"]=sales_id

        for e in body:
            transactions = Transactions(purchases_id=e['purchases_id'], products_id=e['products_id'], sales_id=e['sales_id'], quantity=e['quantity'], warehouses_id=e['warehouses_id'])
            db.session.add(transactions)
        for e in body:
            products = Products.query.get(e['products_id'])
            products.quantity = int(products.quantity) + e['quantity']
        db.session.commit()
        all_transactions = Transactions.query.filter().order_by(Transactions.id)
        all_transactions = list(map(lambda e: e.serialize(), all_transactions))
        return jsonify(all_transactions), 200

    # GET request

    if request.method == 'GET':

        all_transactions = Transactions.query.all()
        all_transactions = list(map(lambda e: e.serialize(), all_transactions))
        return jsonify(all_transactions), 200

    return "Invalid Method", 404



##########################################################################################################
############################################ TRANSACTIONS TABLE ##############################################
##########################################################################################################

############################################ GET ALL / CREATE A NEW ONE TRANSACTIONS ############################################

@app.route('/transactions/new', methods=['GET', 'POST'])

def transactionsNewPost():

    # POST request

    if request.method == 'POST':

        body = request.get_json()
        missing_item = verify_json_single(body,'purchases_id','products_id','quantity')
        if missing_item:
            raise APIException('You need to specify the ' + missing_item, status_code=400)
        transactions = Transactions(purchases_id=body['purchases_id'], products_id=body['products_id'], sales_id=body['sales_id'], quantity=body['quantity'], warehouses_id=body['warehouses_id'])
        products = Products.query.get(body['products_id'])
        products.quantity = int(products.quantity) + body['quantity']
        db.session.add(transactions)
        db.session.commit()
        all_transactions = Transactions.query.filter().order_by(Transactions.id)
        all_transactions = list(map(lambda e: e.serialize(), all_transactions))
        return jsonify(all_transactions), 200

    # GET request

    if request.method == 'GET':

        all_transactions = Transactions.query.all()
        all_transactions = list(map(lambda e: e.serialize(), all_transactions))
        return jsonify(all_transactions), 200

    return "Invalid Method", 404


##########################################################################################################
############################################ WAREHOUSE TABLE ##############################################
##########################################################################################################

############################################ GET ALL WAREHOUSES ############################################

 # ONLY GETTING ALL WAREHOUSES, SINCE THEY ARE HARDCODED IN DB VIA PHPMYADMIN

@app.route('/warehouses/all/', methods=['GET','POST'])

def warehousesAllGet():

# POST request
    if request.method == 'POST':
        body = request.get_json()
        warehouses = Warehouses(warehouse_name=body['warehouse_name'], location=body['location'])
        db.session.add(warehouses)
        db.session.commit()
        all_warehouses = Warehouses.query.filter().order_by(Warehouses.id)
        all_warehouses = list(map(lambda e: e.serialize(), all_warehouses))
        return jsonify(all_warehouses), 200

 # GET request

    all_warehouses = Warehouses.query.all()
    all_warehouses = list(map(lambda e: e.serialize(), all_warehouses))
    return jsonify(all_warehouses), 200


############################################ GET THE TOTAL QTY OF A PARTICULAR WAREHOUSE ############################################
#the id, HAS to be related to a particular product

@app.route('/warehouses/total/<int:warehouse_id>', methods=['GET', 'POST'])

def productsTotalQuantity(warehouse_id):

    gtrans = db.session.query(
    Transactions.warehouses_id,func.sum(Transactions.quantity)
    ).group_by(Transactions.warehouses_id).all()

    gtrans = [list(i) for i in gtrans]

    for t in gtrans:
        print(int(t[1]))

    return str(gtrans[warehouse_id][1]), 200

    #main = 1
    #motorcycle1=1
    #motorcycle2=2
    #motorcycle3=3


############################################ GET THE TOTAL QTY OF ALL WAREHOUSES ############################################
#the id, HAS to be related to a particular product

@app.route('/warehouses/all/total/', methods=['GET', 'POST'])

def productsTotalQuantityAll():

    gtrans = db.session.query(
    Transactions.warehouses_id,func.sum(Transactions.quantity)
    ).group_by(Transactions.warehouses_id).all()

    gtrans = [list(i) for i in gtrans]

    total = int(gtrans[1][1]) + int(gtrans[2][1]) + int(gtrans[3][1]) + int(gtrans[4][1])

   #for t in gtrans:
   #    print(int(t[1]))

    return str(total), 200

    #main = 1
    #motorcycle1=1
    #motorcycle2=2
    #motorcycle3=3

##########################################################################################################
############################################ Jonathan's Login ##############################################
##########################################################################################################

# Setup the Flask-JWT-Simple extension
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)


# Provide a method to create access tokens. The create_jwt()
# function is used to actually generate the token
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    params = request.get_json()
    username = params.get('username', None)
    password = params.get('password', None)

    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    if username != 'test' or password != 'test':
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    ret = {'jwt': create_jwt(identity=username)}
    return jsonify(ret),  200



if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT)

