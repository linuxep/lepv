
"""Module for IO data parsing"""


from flask import Blueprint, jsonify

from app.modules.memory.MemoryProfiler import MemoryProfiler

memoryAPI = Blueprint('memoryAPI', __name__, url_prefix='/api/memory')


@memoryAPI.route('/capacity/<server>', methods=['GET'])
def getMemoryCapacity(server):

    profiler = MemoryProfiler(server)
    data = profiler.getCapacity()

    return jsonify(data)
