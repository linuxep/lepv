
"""Module for CPU Profiler"""


from flask import Blueprint, jsonify, request
from app.modules.cpu.CPUProfiler import CPUProfiler
from app.influxDbUtil.dbUtil import myInfluxDbClient


cpuAPI = Blueprint('cpuAPI', __name__, url_prefix='/api/cpu')


@cpuAPI.route('/capacity/<server>')
def getCpuCapacity(server):

    profiler = CPUProfiler(server)
    data = profiler.getCapacity()

    return jsonify(data)


@cpuAPI.route('/count/<server>')
def getCpuCount(server):

    profiler = CPUProfiler(server)
    data = profiler.getProcessorCount()

    return jsonify(data)


@cpuAPI.route('/status/<server>')
def getCpuStatus(server):

    profiler = CPUProfiler(server)
    data = profiler.getStatus()

    if 'request_id' in request.args:
        data['response_id'] = request.args['request_id']
    return jsonify(data)


@cpuAPI.route('/stat/<server>')
def getCpuStat(server):

    profiler = CPUProfiler(server)
    data = profiler.get_stat()

    if 'request_id' in request.args:
        data['response_id'] = request.args['request_id']
    return jsonify(data)


@cpuAPI.route('/top/<server>')
def getCpuTop(server):

    profiler = CPUProfiler(server)
    data = profiler.getTopOutput()

    if 'request_id' in request.args:
        data['response_id'] = request.args['request_id']
    return jsonify(data)


@cpuAPI.route('/avgload/<server>')
def get_average_load(server):
    # options = {
    #     'is_debug': False,
    # }
    # if not request.args['debug']:
    #     options['is_debug'] = request.args['debug']

    profiler = CPUProfiler(server)
    data = profiler.get_average_load()

    if 'request_id' in request.args:
        data['response_id'] = request.args['request_id']
    client = myInfluxDbClient()
    client.write_points(str(data))
    return jsonify(data)
