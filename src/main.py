import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Bill
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity)
import datetime

app = Flask(__name__)
jwt = JWTManager(app)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route("/login", methods=["POST"])
def handle_login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request / Falta JSON en la solicitud"}), 400
    params = request.get_json()
    email = params.get('email', None)
    password = params.get('password', None)
    if not email:
        return jsonify({"msg": "Missing email parameter / Falta el parametro de correo electronico"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter / Falta el parametro de contrasena"}), 400
    user = User.query.filter_by(email=email).one_or_none()
    if not user:
        return jsonify({"msg": "User does not exist / El usuario no existe"}), 404
    if user.check_password(password):
        jwt= create_access_token(identity=user.id)
        ret = user.serialize()
        ret["jwt"]=jwt
        return jsonify(ret), 200
    else:
        return jsonify({"msg": "Bad credentials / Credenciales incorrectas"}), 401
    
@app.route('/bills/<int:id_user>', methods=['GET'])
##@jwt_required()
def handle_bills(id_user):
    bills = Bill.query.filter_by(user_id=id_user)
    print(bills)
    if bills is None:
        return "NO EXISTE", 404
    if id_user is None:
        raise APIException('You need to specify an existing user', status_code=400)
    response_body= []
    for bill in bills:
        response_body.append(bill.serialize())
    return jsonify(response_body),200

@app.route('/bills', methods=['POST'])
#@jwt_required()
def add_new_bill():
    #email = get_jwt_identity()
    body= request.get_json()
    #validaciones de body para campos obligatorios
    if isinstance (body,dict):
        if body is None:
            raise APIException("Please specify the request body as a json object", status_code=400)
        if 'value' not in body:
            raise APIException("You need to specify the value", status_code=400)
        if 'user_id' not in body:
            raise APIException("You need to specify the id user", status_code=400)
        if 'type' not in body:
            raise APIException("You need to specify the type", status_code=400)
        if 'observation' not in body:
            raise APIException("You need to specify the id observation", status_code=400)

    else: return "error in body, is not a dictionary"
    now = datetime.datetime.now()
    bill = Bill.create_bill(
        date_bill = now,
        user_id=body['user_id'],
        value=body['value'],
        type=body['type'],
        observation=+body['observation'],
    )
    return bill.serialize(), 200

@app.route('/bills/<int:id_bill>', methods=['PATCH'])
#@jwt_required()
def upgrade_bill(id_bill):
    body = request.get_json()
    bill_to_upgrade = Bill.query.get(id_bill)
    if bill_to_upgrade is None:
        raise APIException('You need to specify an existing bill', status_code=400)
    if 'value' in body  != None:
        new_value = body['value']
        bill_to_upgrade.value = new_value
    if 'type' in body  != None:
        new_type = body['type']
        bill_to_upgrade.type = new_type
    if 'observation' in body != None:
        new_observation = body['observation']
        bill_to_upgrade.observation = new_observation

    db.session.commit()
    return 'Cambio realizado'


@app.route('/bills/<int:id_bill>', methods=['DELETE'])
#@jwt_required()
def delete_bill(id_bill): 
    db.session.delete(Bill.query.get_or_404(id_bill) )
    db.session.commit() 
    return '', 204


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
