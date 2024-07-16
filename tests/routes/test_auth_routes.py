# tests/test_auth_routes.py

import pytest
from unittest.mock import patch
from flask import Flask, jsonify

from app.routes.auth_routes import auth_bp
