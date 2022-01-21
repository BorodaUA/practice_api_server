from flask import Blueprint

hello_world_bp = Blueprint('hello_world', 'bp_wtf')


@hello_world_bp.get('/')
def hello_world():
    return {'message': 'Hello world.'}
