from modules.utils.socketIOBlueprint import SocketIOBlueprint
from modules.profilers.io.IOProfiler import IOProfiler
from modules.utils.soketProcessor import process_socket_request, background_timer_stuff
from threading import Timer
from flask_socketio import emit

io_blueprint = SocketIOBlueprint('')

io_status_timer = None
@io_blueprint.on('io.status.req')
def get_io_status(request):
    server = request['server']
    interval = request['interval']
    socketio = io_blueprint.get_io()
    global io_status_timer
    if io_status_timer is None:
        io_status_timer = Timer(interval, background_timer_stuff, [
                                socketio, interval, "io.status.res", IOProfiler(server).get_status])
        io_status_timer.start()
    emit("io.status.res", IOProfiler(server).get_status())
    # process_socket_request(request, 'io.status.req', IOProfiler(server).get_status)

io_top_timer = None
@io_blueprint.on('io.top.req')
def get_io_top(request):
    server = request['server']
    interval = request['interval']
    socketio = io_blueprint.get_io()
    global io_top_timer
    if io_top_timer is None:
        io_top_timer = Timer(interval, background_timer_stuff, [
                             socketio, interval, "io.top.res", IOProfiler(server).get_io_top])
        io_top_timer.start()
    emit("io.top.res", IOProfiler(server).get_io_top())
    # process_socket_request(request, 'io.top.req', IOProfiler(server).get_io_top)
