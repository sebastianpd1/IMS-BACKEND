import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap, verify_json
from models import db, Products, Purchases, Transactions

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
        missing_item = verify_json(body,'item','description')
        if missing_item:
            raise APIException('You need to specify the ' + missing_item, status_code=400)
        products = Products(item=body['item'], description=body['description'])
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

############################################ GET ALL PURCHASES ############################################


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
############################################ TRANSACTIONS TABLE ##############################################
##########################################################################################################

############################################ GET ALL / CREATE A NEW ONE TRANSACTIONS ############################################

@app.route('/transactions/new', methods=['GET', 'POST'])

def transactionsNewPost():

    # POST request

    if request.method == 'POST':

        body = request.get_json()
        missing_item = verify_json(body,'purchases_id','products_id','quantity')
        if missing_item:
            raise APIException('You need to specify the ' + missing_item, status_code=400)
        transactions = Transactions(purchases_id=body['purchases_id'], products_id=body['products_id'], quantity=body['quantity'])
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


############################################ GET ALL / CREATE A NEW ONE TRANSACTIONS ############################################




############################################ PURCHASES TABLE ############################################


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT)