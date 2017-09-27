
"""Module for CPU data parsing"""


from flask import Blueprint, jsonify

from app.modules.cpu.CPUProfiler import CPUProfiler

cpuAPI = Blueprint('cpuAPI', __name__, url_prefix='/api/cpu')


@cpuAPI.route('/count/<server>', methods=['GET'])
def getCpuCount(server):

    profiler = CPUProfiler(server)
    data = profiler.getProcessorCount()

    return jsonify(data)
