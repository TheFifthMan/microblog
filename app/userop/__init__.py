from flask import Blueprint
user_bp = Blueprint('userop',__name__)
from app.userop import routes,forms