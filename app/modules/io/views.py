
"""Module for IO Profiler"""


from flask import Blueprint, jsonify

from modules.io.IOProfiler import IOProfiler

ioAPI = Blueprint('ioAPI', __name__, url_prefix='/api/io')


@ioAPI.route('/capacity/<server>', methods=['GET'])
def getIOCapacity(server):

    profiler = IOProfiler(server)
    data = profiler.getCapacity()

    return jsonify(data)


@ioAPI.route('/status/<server>', methods=['GET'])
def getIOStatus(server):

    profiler = IOProfiler(server)
    data = profiler.getStatus()

    return jsonify(data)


@ioAPI.route('/top/<server>', methods=['GET'])
def getIOTop(server):
    profiler = IOProfiler(server)
    data = profiler.getIoTopData()

    return jsonify(data)