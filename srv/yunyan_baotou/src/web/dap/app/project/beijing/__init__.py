from flask import Blueprint

bp_beijing = Blueprint('bp_beijing', __name__)

from . import interface
