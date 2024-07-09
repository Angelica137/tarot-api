# -*- coding: utf-8 -*-
from flask import Blueprint

bp = Blueprint('main', __name__)


@bp.route('/')
def hello_world():
    return "Hello, World!"
