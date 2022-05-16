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
    available = db.Column(db.Boolean("available"))
    credit = db.Column(db.Boolean("credit"))

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
            'date': self.date,
            'available': self.available,
            'credit': self.credit
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
            note=json.get('note', None),
            date=json.get('date', None),
            available=json.get('available', True),
            credit=json.get('credit', False)
        )


class Payments(db.Model):
    payment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sale_id = db.Column(db.Integer, ForeignKey('sales.sale_id'), primary_key=True)
    payment_cost = db.Column(db.Integer)
    refund = db.Column(db.Boolean("refund"))
    date = db.Column(db.BigInteger)
    sell_type = db.Column(db.String(100))
    payment_date = db.Column(db.BigInteger)
    description = db.Column(db.String(500))


    def to_dict(self):
        return {
            'payment_id': self.payment_id,
            'sale_id': self.sale_id,
            'payment_cost': self.payment_cost,
            'refund': self.refund,
            'date': self.date,
            'sell_type': self.sell_type,
            'payment_date': self.payment_date,
            'description': self.description
        }

    @staticmethod
    def from_json(json):
        return Payments(
            payment_id=json.get('payment_id', None),
            sale_id=json.get('sale_id', None),
            payment_cost=json.get('payment_cost', None),
            refund=json.get('refund', False),
            date=json.get('date', None),
            sell_type=json.get('sell_type', None),
            payment_date=json.get('payment_date', None),
            description=json.get('description', None)
        )