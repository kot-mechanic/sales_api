from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth



from products_api.model.models import db, Products

# from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://testuser:M7astUUFKxOAxvo88Tb3Bp6JRUJEi1Nv6xfyyy6w@34.125.65.175/products"

auth = HTTPBasicAuth()
user = {'login': 'service', 'password': 'ScaNTestrApToWeITERaCEmanTALaver'}
# db = SQLAlchemy(app)

db.init_app(app)

@auth.verify_password
def verify_password(username, password):
    if username == user['login'] and password == user['password']:
        return username


@app.route('/')
def hello():
    return {"hello": "world"}



@app.route('/products', methods=['POST', 'GET'])
@auth.login_required
def products():
    if request.method == 'POST':
        if request.is_json:
            json = request.get_json()
            new_product = Products.from_json(json)
            db.session.add(new_product)
            db.session.commit()
            return jsonify(new_product.to_dict()), 200
        else:
            return {"error": "The request payload is not in JSON format"}

@app.route('/products/<sale_id>', methods=['POST', 'GET'])
@auth.login_required
def sales(sale_id):
    products = Products.query.filter_by(sale_id=sale_id)
    results = [
            {
                "sale_id": product.sale_id,
                "seller_service_id": product.seller_service_id,
                "user_id": product.user_id,
                "product_id": product.product_id,
                "product_type": product.product_type,
                "rate": product.rate,
                "cost": product.cost,
                "promocode": product.promocode,
                "discount": product.discount,
                "payment_cost": product.payment_cost,
                "note": product.note,
                "date": product.date
            } for product in products]

    return {"products": results}



if __name__ == '__main__':
    app.run(host='192.168.42.113', port=5000)