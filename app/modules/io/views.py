
"""Module for IO Profiler"""

from flask import Blueprint, jsonify, request

from app.modules.io.IOProfiler import IOProfiler

ioAPI = Blueprint('ioAPI', __name__, url_prefix='/api/io')


@ioAPI.route('/capacity/<server>')
def get_io_capacity(server):

    profiler = IOProfiler(server)
    data = profiler.get_capacity()

    if 'request_id' in request.args:
        data['response_id'] = request.args['request_id']

    return jsonify(data)


@ioAPI.route('/status/<server>')
def get_io_status(server):

    profiler = IOProfiler(server)
    data = profiler.get_status()

    if 'request_id' in request.args:
        data['response_id'] = request.args['request_id']

    return jsonify(data)


@ioAPI.route('/top/<server>')
def get_io_top(server):
    profiler = IOProfiler(server)
    data = profiler.get_io_top()

    if 'request_id' in request.args:
        data['response_id'] = request.args['request_id']

    return jsonify(data)