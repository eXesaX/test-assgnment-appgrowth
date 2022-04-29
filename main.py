from datetime import datetime
from unittest.mock import Mock

from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField

app = Flask(__name__)


def get_db():
    """
    Abstract away DB connection init/retrieval
    """
    return Mock()

db = get_db()

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    address = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class OrderRepository:
    """
    DB adapter
    """
    def __init__(self):
        self.db = get_db()

    def create_order(self, **kwargs):
        order = Order(**kwargs)
        self.db.session.add(order)
        self.db.session.commit()


class OrderForm(FlaskForm):
    name = StringField('name')
    address = StringField('address')

    class Meta:
        csrf = False


class CreateOrderService:
    """
    App's business logic
    """
    def create_order(self) -> bool:
        form = OrderForm()
        if form.validate():
            OrderRepository().create_order(**form.data)  # Order model doesn't appear at app level anymore
            return True
        else:
            return False


class CreateOrderHtmlResponse:
    """
    BL to representation adapter
    """
    def get_representation(self, result: bool) -> str:  # 'bool' type here can be replaced with custom type if more context is needed
        if result:
            return "<h1>Success</h1>"
        else:
            return "<h1>Failed</h1>"


@app.route("/create", methods=['POST'])
def create_order():
    return CreateOrderHtmlResponse().get_representation(CreateOrderService().create_order())


