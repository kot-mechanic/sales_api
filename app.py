from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# from sqlalchemy.orm import relationship


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://testuser:M7astUUFKxOAxvo88Tb3Bp6JRUJEi1Nv6xfyyy6w@34.125.65.175/products"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/')
def hello():
    return {"hello": "world"}

class Seller_services(db.Model):
    # __tablename__ = 'seller_services'

    seller_service_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def to_dict(self):
        return {
            'seller_service_id': self.seller_service_id,
            'name': self.name
        }

    @staticmethod
    def from_json(json):
        return Seller_services(
            seller_service_id=json.get('seller_service_id', None),
            name=json.get('name', None)
        )

    # def __repr__(self):
    #     return f""


class Products(db.Model):
    # __tablename__ = 'products'

    sale_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    seller_service_id = db.Column(db.Integer, ForeignKey('seller_services.seller_service_id'), primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    product_type = db.Column(db.String(100))
    rate = db.Column(db.String(20))
    cost = db.Column(db.Integer)
    promocode = db.Column(db.String(100))
    discount = db.Column(db.Integer)
    payment_cost = db.Column(db.Integer)
    note = db.Column(db.String(200))
    date = db.Column(db.BigInteger)

    # def __init__(self, sale_id, seller_service_id, user_id, product_id, product_type, rate, cost, promocode, discount, payment_cost, note, date):
    def to_dict(self):
        return {
            'sale_id': self.sale_id,
            'seller_service_id': self.seller_service_id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'product_type': self.product_type,
            'rate': self.rate,
            'cost': self.cost,
            'promocode': self.promocode,
            'discount': self.discount,
            'payment_cost': self.payment_cost,
            'note': self.note,
            'date': self.date
        }


    # def __repr__(self):
    #     return f""

    @staticmethod
    def from_json(json):
        return Products(
            sale_id=json.get('sale_id', None),
            seller_service_id=json.get('seller_service_id', None),
            user_id=json.get('user_id', None),
            product_id=json.get('product_id', None),
            product_type=json.get('product_type', None),
            rate=json.get('rate', None),
            cost=json.get('cost', None),
            promocode=json.get('promocode', None),
            discount=json.get('discount', True),
            payment_cost=json.get('payment_cost', None),
            note=json.get('note', False),
            date=json.get('date', False)
        )


@app.route('/products', methods=['POST', 'GET'])
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