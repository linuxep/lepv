
"""Module for Perf profiling"""


from flask import Blueprint, jsonify, request

from modules.profilers.perf.PerfProfiler import PerfProfiler

perfAPI = Blueprint('perfAPI', __name__, url_prefix='/api/perf')


@perfAPI.route('/cpu/<server>')
def getPerfCpuClockData(server):

    profiler = PerfProfiler(server)
    data = profiler.getPerfCpuClock()

    if 'request_id' in request.args:
        data['response_id'] = request.args['request_id']

    return jsonify(data)
