from flask import Flask

from model.models import db
from sales_api import sales_blueprint



# from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://salesowner:DESb05XQlEKWdkLGVGjMCNFLhE4oQF@95.165.131.159/sales"

app.register_blueprint(sales_blueprint)

db.init_app(app)

if __name__ == '__main__':
    app.run(host='192.168.42.125', port=5000)