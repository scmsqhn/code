from flask import Blueprint

bp_shandong = Blueprint('bp_shandong', __name__)

from . import interface
