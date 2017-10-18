
"""Module for Memory profiler"""


from flask import Blueprint, jsonify, request

from modules.memory.MemoryProfiler import MemoryProfiler

memoryAPI = Blueprint('memoryAPI', __name__, url_prefix='/api/memory')


@memoryAPI.route('/capacity/<server>')
def getMemoryCapacity(server):

    profiler = MemoryProfiler(server)
    data = profiler.getCapacity()

    if 'request_id' in request.args:
        data['response_id'] = request.args['request_id']

    return jsonify(data)


@memoryAPI.route('/status/<server>')
def getMemoryStatus(server):

    profiler = MemoryProfiler(server)
    data = profiler.getStatus()

    if 'request_id' in request.args:
        data['response_id'] = request.args['request_id']

    return jsonify(data)


@memoryAPI.route('/procrank/<server>')
def getMemoryProcrank(server):

    profiler = MemoryProfiler(server)
    data = profiler.getProcrank()

    if 'request_id' in request.args:
        data['response_id'] = request.args['request_id']

    return jsonify(data)