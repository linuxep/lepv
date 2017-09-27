
"""Module for Perf profiling"""


from flask import Blueprint, jsonify

from modules.perf.PerfProfiler import PerfProfiler

perfAPI = Blueprint('perfAPI', __name__, url_prefix='/api/perf')


@perfAPI.route('/cpu/<server>', methods=['GET'])
def getPerfCpuClockData(server):

    profiler = PerfProfiler(server)
    data = profiler.getPerfCpuClock()

    return jsonify(data)
