from flask import Blueprint, request, jsonify
from flask_httpauth import HTTPBasicAuth
import time

from model.models import db, Payments

payments_blueprint = Blueprint('payments_blueprint', __name__)

auth = HTTPBasicAuth()
user = {'login': 'service', 'password': 'ScaNTestrApToWeITERaCEmanTALaver'}

@auth.verify_password
def verify_password(username, password):
    if username == user['login'] and password == user['password']:
        return username

@payments_blueprint.route('/payments', methods=['POST', 'GET'])
@auth.login_required
def payments():
# Добавление информации о продаже
    if request.method == 'POST':
        if request.is_json:
            json = request.get_json()
            # print(json)
            json['date'] = int(time.time())
            new_payment = Payments.from_json(json)
            # print(new_payment)
            db.session.add(new_payment)
            db.session.commit()
            return jsonify(new_payment.to_dict()), 200
        else:
            return {"error": "The request payload is not in JSON format"}
# Чтение списка sale_id+date по всем продажам
#     if request.method == 'GET':
#         s = Sales.query.with_entities(Sales.sale_id, Sales.date).all()
#         results = [
#             {
#                 "sale_id": sale.sale_id,
#                 "date": sale.date
#             } for sale in s]
#         return {"sales": results}, 200