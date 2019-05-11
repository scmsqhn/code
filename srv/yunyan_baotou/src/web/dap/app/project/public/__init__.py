from flask import Blueprint

bp_public = Blueprint('bp_public', __name__)

from . import interface