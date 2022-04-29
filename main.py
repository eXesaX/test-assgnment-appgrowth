from datetime import datetime

from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
app = Flask('name')

# let's assume that there is db and migrated
db = app.db


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    address = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class OrderForm(FlaskForm):
    name = StringField('name')
    address = StringField('address')


@app.route("/create", methods=['POST'])
def create_order():
    form = OrderForm()
    if form.validate():
        order = Order()
        form.populate_obj(order)
        db.session.add(order)
        db.session.commit()
        return "<h1>Success</h1>"
    else:
        return "<h1>Failed</h1>"


# Task:
# implement based on hexagonal architecture
# mamba + expects + mocks tests for the service
# Reference:
# https://medium.com/@vsavkin/hexagonal-architecture-for-rails-developers-8b1fee64a613
# https://en.wikipedia.org/wiki/Hexagonal_architecture_(software)
# https://www.youtube.com/watch?v=tg5RFeSfBM4
