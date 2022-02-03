from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
import time


from products_api.model.models import db, Sales, Seller_services

# from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://salesowner:salesowner@192.168.42.134/sales"

auth = HTTPBasicAuth()
user = {'login': 'service', 'password': 'ScaNTestrApToWeITERaCEmanTALaver'}
# db = SQLAlchemy(app)

db.init_app(app)

@auth.verify_password
def verify_password(username, password):
    if username == user['login'] and password == user['password']:
        return username

@app.route('/seller_services', methods=['POST', 'GET'])
@auth.login_required
def get_seller_services():
    if request.method == 'GET':
        ss = Seller_services.query.all()
        results = [
                {
                'seller_service_id': s.seller_service_id,
                'name': s.name
                } for s in ss]
        return {"seller_services": results}

    if request.method == 'POST':
        json = request.get_json()
        ss = Seller_services.from_json(json)
        db.session.add(ss)
        db.session.commit()
        return jsonify(ss.to_dict()), 200

@app.route('/sales', methods=['POST', 'GET'])
@auth.login_required
def products():
    if request.method == 'POST':
        if request.is_json:
            json = request.get_json()
            json['date'] = int(time.time())
            new_sale = Sales.from_json(json)
            db.session.add(new_sale)
            db.session.commit()
            return jsonify(new_sale.to_dict()), 200
        else:
            return {"error": "The request payload is not in JSON format"}

    if request.method == 'GET':
        s = Sales.query.with_entities(Sales.sale_id, Sales.date).all()
        print(s)
        # print(jsonify(s.to_dict()))
        # print(jsonify(s.sale_id.to_dict(), s.date.to_dict()))
        # return jsonify(sale_id=s.sale_id, date=s.date), 200
        # return jsonify(sale_id=s[0], date=s[1]), 200
        # return jsonify(s.to_dict(sale_id, date)), 200
        return jsonify(s), 200
        # return {"sales": jsonify(s)}, 200
    # {"sales": results}

@app.route('/sales/<sale_id>', methods=['POST', 'GET'])
@auth.login_required
def sales(sale_id):
    if request.method == 'GET':
        sales = Sales.query.filter_by(sale_id=sale_id)
        results = [
                {
                "sale_id": sale.sale_id,
                "seller_service_id": sale.seller_service_id,
                "user_id": sale.user_id,
                "product_id": sale.product_id,
                "product_type": sale.product_type,
                "rate": sale.rate,
                "cost": sale.cost,
                "promocode": sale.promocode,
                "discount": sale.discount,
                "payment_cost": sale.payment_cost,
                "note": sale.note,
                "date": sale.date
                } for sale in sales]
        return {"sale": results}

    # if request.method == 'POST':

@app.route('/sales/sales', methods=['GET'])
@auth.login_required
def getsales():
    if request.method == 'GET':
        json = request.get_json()
        saleid = json.get('sale_id')
        print(str(saleid))
        # p = Sales.query.filter_by(sale_id in (saleid))
        # print(p)



if __name__ == '__main__':
    app.run(host='192.168.42.113', port=5000)