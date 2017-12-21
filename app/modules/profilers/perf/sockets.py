from modules.utils.socketIOBlueprint import SocketIOBlueprint
from modules.profilers.perf.PerfProfiler import PerfProfiler
from modules.utils.soketProcessor import process_socket_request, background_timer_stuff
from threading import Timer
from flask_socketio import emit

perf_blueprint = SocketIOBlueprint('')

perf_cpuclock_timer = None
@perf_blueprint.on('perf.cpuclock.req')
def get_perf_cpu_clock(request):
    server = request['server']
    interval = request['interval']
    socketio = perf_blueprint.get_io()
    global perf_cpuclock_timer
    if perf_cpuclock_timer is None:
        perf_cpuclock_timer = Timer(interval, background_timer_stuff, [
            socketio, interval, "perf.cpuclock.res", PerfProfiler(server).get_perf_cpu_clock])
        perf_cpuclock_timer.start()
    emit("perf.cpuclock.res", PerfProfiler(server).get_perf_cpu_clock())
    # process_socket_request(request, 'perf.cpuclock.req', PerfProfiler(server).get_perf_cpu_clock)


perf_flame_timer = None
@perf_blueprint.on('perf.flame.req')
def get_perf_flame(request):
    server = request['server']
    interval = request['interval']
    socketio = perf_blueprint.get_io()
    global perf_flame_timer
    if perf_flame_timer is None:
        perf_flame_timer = Timer(interval, background_timer_stuff, [
            socketio, interval, "perf.flame.res", PerfProfiler(server).get_cmd_perf_flame])
        perf_flame_timer.start()
    emit("perf.flame.res", PerfProfiler(server).get_cmd_perf_flame())
    # process_socket_request(request, 'perf.flame.req', PerfProfiler(server).get_cmd_perf_flame)
