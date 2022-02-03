from sqlalchemy import ForeignKey
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate

db = SQLAlchemy()
# migrate = Migrate(app, db)



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


class Sales(db.Model):
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
        return Sales(
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
