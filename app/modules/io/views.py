
"""Module for IO data parsing"""


from flask import Blueprint, jsonify

from app.modules.io.IOProfiler import IOProfiler

ioAPI = Blueprint('ioAPI', __name__, url_prefix='/api/io')


@ioAPI.route('/capacity/<server>', methods=['GET'])
def getIOCapacity(server):

    profiler = IOProfiler(server)
    data = profiler.getCapacity()

    return jsonify(data)
