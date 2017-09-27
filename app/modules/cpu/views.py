
"""Module for CPU Profiler"""


from flask import Blueprint, jsonify

from app.modules.cpu.CPUProfiler import CPUProfiler

cpuAPI = Blueprint('cpuAPI', __name__, url_prefix='/api/cpu')


@cpuAPI.route('/capacity/<server>', methods=['GET'])
def getCpuCapacity(server):

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
    data = profiler.getStat()

    return jsonify(data)


@cpuAPI.route('/top/<server>', methods=['GET'])
def getCpuTop(server):

    profiler = CPUProfiler(server)
    data = profiler.getTopOutput()

    return jsonify(data)


@cpuAPI.route('/avgload/<server>', methods=['GET'])
def getAverageLoad(server):

    profiler = CPUProfiler(server)
    data = profiler.getAverageLoad()

    return jsonify(data)