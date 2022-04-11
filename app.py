from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
import time


from model.models import db, Sales, Seller_services

# from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://salesowner:DESb05XQlEKWdkLGVGjMCNFLhE4oQF@95.165.131.159/sales"

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
# Получить список seller_services
    if request.method == 'GET':
        ss = Seller_services.query.all()
        results = [
                {
                'seller_service_id': s.seller_service_id,
                'name': s.name
                } for s in ss]
        return {"seller_services": results}
# Добавить seller_services
    if request.method == 'POST':
        json = request.get_json()
        ss = Seller_services.from_json(json)
        db.session.add(ss)
        db.session.commit()
        return jsonify(ss.to_dict()), 200

@app.route('/sales', methods=['POST', 'GET'])
@auth.login_required
def sales():
# Добавление информации о продаже
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
# Чтение списка sale_id+date по всем продажам
    if request.method == 'GET':
        s = Sales.query.with_entities(Sales.sale_id, Sales.date).all()
        results = [
            {
                "sale_id": sale.sale_id,
                "date": sale.date
            } for sale in s]
        return {"sales": results}, 200


@app.route('/sales/<sale_id>', methods=['POST', 'GET', 'DELETE'])
@auth.login_required
def saleinfo(sale_id):
    sales = Sales.query.filter_by(sale_id=sale_id)
# Получение информации по конкретной продаже
    if request.method == 'GET':
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
        return {"sale": results}, 200
# Обновление информации по продаже
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({'error': 'Body is not json.', 'success': None}), 403
        json = request.get_json()
        json['date'] = int(time.time())
        sales.update(json)
        db.session.commit()
        return jsonify(sales.first().to_dict()), 200
# Удаление информации о продаже
    if request.method == 'DELETE':
        result = sales.delete()
        db.session.commit()
        return jsonify({'error': None, 'success': result}), 200


@app.route('/sales/multiple_sales', methods=['GET'])
@auth.login_required
def getsales():
# Получение информации по нескольким продажам
    if request.method == 'GET':
        json = request.get_json()
        saleid = json.get('sale_id')
        sales = Sales.query.filter(Sales.sale_id.in_(saleid)).all()
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
        return {"sale": results}, 200


@app.route('/sales/request', methods=['GET'])
@auth.login_required
def custom_request():
    json = request.get_json()
    user_id = json.get('user_id')
    product_type = json.get('product_type')
    product_id = json.get('product_id')
    sale_id = json.get('sale_id')
    # sales = Sales.query.filter_by(user_id=user_id, product_type=product_type, product_id=product_id).order_by(Sales.sale_id.desc()).limit(3)
    if user_id is not None and product_type is not None and product_id is not None and sale_id is not None:
        sales = Sales.query.filter(Sales.user_id==user_id, Sales.product_type==product_type, Sales.product_id==product_id, Sales.sale_id < sale_id).order_by(Sales.sale_id.desc()).limit(3)
    if user_id is not None and product_type is not None and product_id is None and sale_id is not None:
        sales = Sales.query.filter(Sales.user_id == user_id, Sales.product_type == product_type, Sales.sale_id < sale_id).order_by(Sales.sale_id.desc()).limit(3)
    if user_id is not None and product_type is not None and product_id is not None and sale_id is None:
        sales = Sales.query.filter(Sales.user_id==user_id, Sales.product_type==product_type, Sales.product_id==product_id).order_by(Sales.sale_id.desc()).limit(3)
    if user_id is not None and product_type is None and product_id is not None and sale_id is not None:
        sales = Sales.query.filter(Sales.user_id==user_id, Sales.product_id==product_id, Sales.sale_id < sale_id).order_by(Sales.sale_id.desc()).limit(3)
    if user_id is  None and product_type is not None and product_id is not None and sale_id is not None:
        sales = Sales.query.filter(Sales.product_type==product_type, Sales.product_id==product_id, Sales.sale_id < sale_id).order_by(Sales.sale_id.desc()).limit(3)

# Получение информации по конкретной продаже
    if request.method == 'GET':
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
        return {"sale": results}, 200


if __name__ == '__main__':
    app.run(host='192.168.42.125', port=5000)