import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap, verify_json
from models import db, Products

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

@app.route('/products/all', methods=['GET', 'DELETE'])

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
        all_products = list(map(lambda item: item.serialize(), all_products))
        return jsonify(all_products), 200

    # GET request

    if request.method == 'GET':

        all_products = Products.query.all()
        all_products = list(map(lambda item: item.serialize(), all_products))
        return jsonify(all_products), 200

    return "Invalid Method", 404


############################################ SALES TABLE ################################################

############################################ PURCHASES TABLE ############################################


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT)