
"""Module for CPU Profiler"""


from flask import Blueprint, jsonify, request
from modules.cpu.CPUProfiler import CPUProfiler

cpuAPI = Blueprint('cpuAPI', __name__, url_prefix='/api/cpu')


@cpuAPI.route('/capacity/<server>', methods=['GET'])
def getCpuCapacity(server):
    # options = {
    #     'is_debug': False,
    #     'request_id': 0
    # }
    # if not request.args['debug']:
    #     options['is_debug'] = request.args['debug']
    # if not request.args['request_id']:
    #     options['request_id'] = request.args['request_id']

    profiler = CPUProfiler(server)
    data = profiler.getCapacity()

    return jsonify(data)


@cpuAPI.route('/count/<server>', methods=['GET'])
def getCpuCount(server):

    profiler = CPUProfiler(server)
    data = profiler.getProcessorCount()

    return jsonify(data)


@cpuAPI.route('/status/<server>', methods=['GET'])
def getCpuStatus(server):

    profiler = CPUProfiler(server)
    data = profiler.getStatus()

    return jsonify(data)


@cpuAPI.route('/stat/<server>', methods=['GET'])
def getCpuStat(server):

    profiler = CPUProfiler(server)
    data = profiler.get_stat()

    return jsonify(data)


@cpuAPI.route('/top/<server>', methods=['GET'])
def getCpuTop(server):

    profiler = CPUProfiler(server)
    data = profiler.getTopOutput()

    return jsonify(data)

@cpuAPI.route('/avgload/<server>')
def getAverageLoad(server):

    profiler = CPUProfiler(server)
    data = profiler.getAverageLoad()

    return jsonify(data)

