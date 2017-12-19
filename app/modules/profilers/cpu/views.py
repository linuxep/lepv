
"""Module for CPU Profiler"""
from flask import Blueprint, jsonify, request
from modules.profilers.cpu.CPUProfiler import CPUProfiler

cpuAPI = Blueprint('cpuAPI', __name__, url_prefix='/api/cpu')

# @socketio.on('client_connected')
# def handle_my_custom_event(json):
#     print('received json: ' + str(json))
#     emit('server_confirmed', "socket io response!!!!!")

# @socketio.on('joined', namespace='/chat')
# def joined(message):
#     """Sent by clients when they enter a room.
#     A status message is broadcast to all people in the room."""
#     room = session.get('room')
#     join_room(room)
#     emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)


@cpuAPI.route('/capacity/<server>')
def getCpuCapacity(server):

    profiler = CPUProfiler(server)
    data = profiler.get_capacity()

    return jsonify(data)


@cpuAPI.route('/count/<server>')
def getCpuCount(server):

    profiler = CPUProfiler(server)
    data = profiler.get_processor_count()

    return jsonify(data)


@cpuAPI.route('/status/<server>')
def getCpuStatus(server):

    profiler = CPUProfiler(server)

    data = profiler.get_status()

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
    return jsonify(data)



