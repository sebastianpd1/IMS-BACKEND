import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from sqlalchemy import func
from utils import APIException, generate_sitemap, verify_json, verify_json_single, get_lat_long
from models import db, Products, Purchases, Sales, Transactions, Warehouses, User
import json
from flask_jwt_simple import JWTManager, jwt_required, create_jwt, get_jwt_identity
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import requests

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
        warehouses = Warehouses(warehouse_name=body['warehouse_name'])
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
    usercheck = User.query.filter_by(username=username, password=password).first()
    if usercheck == None:
        return jsonify({"msg": "Bad username or password"}), 401
    # Identity can be any data that is json serializable
    ret = {'jwt': create_jwt(identity=username)}
    return jsonify(ret),  200

@app.route('/user', methods=['POST', 'GET'])
# @jwt_required
def handle_user():
    """
    Create user and retrieve all users
    """
    # POST request
    if request.method == 'POST':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'username' not in body:
            raise APIException('You need to specify the username', status_code=400)
        if 'password' not in body:
            raise APIException('You need to specify the password', status_code=400)
        user1 = User(username=body['username'], email=body['email'], name=body['name'], last_name=body['last_name'], password=body['password'])
        db.session.add(user1)
        db.session.commit()
        return "The User was added.", 200
    # GET request
    if request.method == 'GET':
        all_people = User.query.all()
        all_people = list(map(lambda x: x.serialize(), all_people))
        return jsonify(all_people), 200
    return "Invalid Method", 404

@app.route('/user/<int:user_id>', methods=['PUT', 'GET', 'DELETE'])
def get_single_user(user_id):
    """
    Single user
    """
    # PUT request
    if request.method == 'PUT':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        user1 = User.query.get(user_id)
        if user1 is None:
            raise APIException('User not found', status_code=404)
        if "username" in body:
            user1.username = body["username"]
        if "email" in body:
            user1.email = body["email"]
        if "password" in body:
            user1.password = body["password"]
        if "last_name" in body:
            user1.last_name = body["last_name"]
        if "name" in body:
            user1.name = body["name"]
        db.session.commit()
        return jsonify(user1.serialize()), 200
    # GET request
    if request.method == 'GET':
        user1 = User.query.get(user_id)
        if user1 is None:
            raise APIException('User not found', status_code=404)
        return jsonify(user1.serialize()), 200
    # DELETE request
    if request.method == 'DELETE':
        user1 = User.query.get(user_id)
        if user1 is None:
            raise APIException('User not found', status_code=404)
        db.session.delete(user1)
        db.session.commit()
        return "ok", 200
    return "Invalid Method", 404

##########################################################################################################
############################################ TWILIO AND GPS ##############################################
##########################################################################################################

############################################ Send SMS from Backend to twilio ##############################################

@app.route('/smstotwilio/<int:warehouse_id>', methods=['PUT', 'GET', 'DELETE'])
def sendSms(warehouse_id):
    # Your Account Sid and Auth Token from twilio.com/console
    # DANGER! This is insecure. See http://twil.io/secure
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    if(warehouse_id==1):

        client = Client(account_sid, auth_token)

        message = client.messages \
                        .create(
                            body="999",
                            from_='+13346058062',
                            to='+17865577374'
                        )

        print(message.sid)

        return "ok", 200

############################################ Send SMS from device to twilio to backend ##############################################

@app.route("/receivefromtwilio", methods=['GET', 'POST'])

def sms():

    number = request.form['From']
    print(number)
    sms_text = request.form['Body']
    print(sms_text)

    bike = 1
    if number == '+17865577374':
        bike = 1
    url = sms_text[sms_text.find(',')+1:]
    print(url)
    response = requests.get(url)
    html_source_code = response.text

    coord = get_lat_long(html_source_code)
    print(coord["latitude"])
    print(coord["longitude"])
    if coord is None:
        return jsonify({ "msg": "Imposible to fetch latitude and longitud" }), 400
    warehouse = Warehouses.query.get(bike)
    warehouse.latitude = str(coord["latitude"])
    warehouse.longitude = str(coord["longitude"])

    db.session.commit()
    all_warehouses = Warehouses.query.filter().order_by(Warehouses.id)
    all_warehouses = list(map(lambda e: e.serialize(), all_warehouses))

    return jsonify(all_warehouses), 200


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT)