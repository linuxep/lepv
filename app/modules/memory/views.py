
"""Module for Memory profiler"""


from flask import Blueprint, jsonify

from modules.memory.MemoryProfiler import MemoryProfiler

memoryAPI = Blueprint('memoryAPI', __name__, url_prefix='/api/memory')


@memoryAPI.route('/capacity/<server>', methods=['GET'])
def getMemoryCapacity(server):

    profiler = MemoryProfiler(server)
    data = profiler.getCapacity()

    return jsonify(data)


@memoryAPI.route('/status/<server>', methods=['GET'])
def getMemoryStatus(server):

    profiler = MemoryProfiler(server)
    data = profiler.getStatus()

    return jsonify(data)


@memoryAPI.route('/procrank/<server>', methods=['GET'])
def getMemoryProcrank(server):

    profiler = MemoryProfiler(server)
    data = profiler.getProcrank()

    return jsonify(data)