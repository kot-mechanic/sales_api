from flask import Blueprint, request, jsonify
from flask_httpauth import HTTPBasicAuth
import time
import psycopg2



from model.models import db, Payments, Sales

payments_blueprint = Blueprint('payments_blueprint', __name__)

auth = HTTPBasicAuth()
user = {'login': 'service', 'password': 'ScaNTestrApToWeITERaCEmanTALaver'}

@auth.verify_password
def verify_password(username, password):
    if username == user['login'] and password == user['password']:
        return username

@payments_blueprint.route('/payments', methods=['POST', 'GET', 'DELETE'])
@auth.login_required
def payments():
# Добавление информации об оплате
    if request.method == 'POST':
        if request.is_json:
            json = request.get_json()
            conn = psycopg2.connect(host="95.165.131.159", database="sales", user="salesowner", password="DESb05XQlEKWdkLGVGjMCNFLhE4oQF")
            update_sale = """update sales set payment_cost=payment_cost+'"""+str(json['payment_cost'])+"""', date='"""+str(int(time.time()))+"""' where sale_id="""+str(json['sale_id'])
            cur = conn.cursor()
            cur.execute(update_sale)
            # cur.execute("""commit""")
            conn.commit()
            conn.close()
            json['date'] = int(time.time())
            new_payment = Payments.from_json(json)
            # print(new_payment)
            db.session.add(new_payment)
            db.session.commit()
            return jsonify(new_payment.to_dict()), 200
        else:
            return {"error": "The request payload is not in JSON format"}
# Удаление информации об оплате
    if request.method == 'DELETE':
        if request.is_json:
            json = request.get_json()
            # check_payment_exist(str(json['payment_id']))
            payment_data = Payments.query.filter_by(payment_id=json['payment_id']).first()
            if payment_data is None:
                return {"error": "Payment_id "+str(json['payment_id'])+" does not exist"}
            if payment_data is not None:
                conn = psycopg2.connect(host="95.165.131.159", database="sales", user="salesowner", password="DESb05XQlEKWdkLGVGjMCNFLhE4oQF")
                update_sale = """update sales set payment_cost=payment_cost-(select payment_cost from payments where payment_id='"""+str(json['payment_id'])+"""'), date='"""+str(int(time.time()))+"""' where sale_id=(select sale_id from payments where payment_id='"""+str(json['payment_id'])+"""')"""
                cur = conn.cursor()
                cur.execute(update_sale)
                conn.commit()
                conn.close()
                json['date'] = int(time.time())
                payment_data = Payments.query.filter_by(payment_id=json['payment_id']).first()
                db.session.delete(payment_data)
                db.session.commit()
                return jsonify(payment_data.to_dict()), 200
        else:
            return {"error": "The request payload is not in JSON format"}


@payments_blueprint.route('/payments/payment_id/<payment_id>', methods=['POST'])
@auth.login_required
def paymentinfo_by_p(payment_id):
    if request.method == 'POST':
        data = Payments.query.filter_by(payment_id=payment_id).all()
        results = [
            {
                "payment_id": payment.payment_id,
                "sale_id": payment.sale_id,
                "payment_cost": payment.payment_cost,
                "refund": payment.refund,
                "date": payment.date
            } for payment in data]
        return {"payments": results}, 200

@payments_blueprint.route('/payments/sale_id/<sale_id>', methods=['POST'])
@auth.login_required
def paymentinfo_by_s(sale_id):
    if request.method == 'POST':
        data = Payments.query.filter_by(sale_id=sale_id).all()
        results = [
            {
                "payment_id": payment.payment_id,
                "sale_id": payment.sale_id,
                "payment_cost": payment.payment_cost,
                "refund": payment.refund,
                "date": payment.date
            } for payment in data]
        return {"payments": results}, 200

# def check_payment_exist(payment_id):
#     payment_data = Payments.query.filter_by(payment_id=payment_id).first()
#     print(payment_data)