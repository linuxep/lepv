
"""Module for IO Profiler"""

from flask import Blueprint, jsonify

from modules.io.IOProfiler import IOProfiler

ioAPI = Blueprint('ioAPI', __name__, url_prefix='/api/io')


@ioAPI.route('/capacity/<server>', methods=['GET'])
def get_io_capacity(server):

    profiler = IOProfiler(server)
    data = profiler.get_capacity()

    return jsonify(data)


@ioAPI.route('/status/<server>', methods=['GET'])
def get_io_status(server):

    profiler = IOProfiler(server)
    data = profiler.get_status()

    return jsonify(data)


@ioAPI.route('/top/<server>', methods=['GET'])
def get_io_top(server):
    profiler = IOProfiler(server)
    data = profiler.get_io_top()

    return jsonify(data)