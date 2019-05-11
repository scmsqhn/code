from flask import Blueprint

bp_guizhou = Blueprint('bp_guizhou', __name__)

from . import interface
