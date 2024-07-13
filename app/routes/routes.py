# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request
from app.models.card_model import Card
from app.models.spread_model import Spread
from app.models.spread_layout_model import SpreadLayout
from app import db


api = Blueprint('api', __name__)


@api.route('/')
def hello_world():
    return "Hello, World!"
