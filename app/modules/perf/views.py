
"""Module for IO data parsing"""


from flask import Blueprint, jsonify

from app.modules.perf.PerfProfiler import PerfProfiler

perfAPI = Blueprint('perfAPI', __name__, url_prefix='/api/perf')


@perfAPI.route('/cpu/<server>', methods=['GET'])
def getPerfCpuClockData(server):

    profiler = PerfProfiler(server)
    data = profiler.getPerfCpuClock()

    return jsonify(data)
