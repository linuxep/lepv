from modules.utils.socketIOBlueprint import SocketIOBlueprint
from modules.profilers.cpu.CPUProfiler import CPUProfiler
from modules.utils.soketProcessor import process_socket_request, background_timer_stuff
from flask_socketio import emit
from threading import Timer

cpu_blueprint = SocketIOBlueprint('')

cpu_stat_timer = None
@cpu_blueprint.on('cpu.stat.req')
def get_cpu_stat(request):
    server = request['server']
    interval = request['interval']
    socketio = cpu_blueprint.get_io()
    global cpu_stat_timer
    if cpu_stat_timer is None:
        cpu_stat_timer = Timer(interval, background_timer_stuff, [socketio, interval, "cpu.stat.res", CPUProfiler(server).get_irq])
        cpu_stat_timer.start()
    emit("cpu.stat.res", CPUProfiler(server).get_irq())


cpu_softirq_timer = None
@cpu_blueprint.on('cpu.softirq.req')
def get_cpu_softirq(request):
    server = request['server']
    interval = request['interval']
    socketio = cpu_blueprint.get_io()
    global cpu_softirq_timer
    if cpu_softirq_timer is None:
        cpu_softirq_timer = Timer(interval, background_timer_stuff, [socketio, interval, "cpu.softirq.res", CPUProfiler(server).get_softirq])
        cpu_softirq_timer.start()
    emit("cpu.softirq.res", CPUProfiler(server).get_softirq())

cpu_status_timer = None
@cpu_blueprint.on('cpu.status.req')
def get_cpu_status(request):
    server = request['server']
    interval = request['interval']
    socketio = cpu_blueprint.get_io()
    global cpu_status_timer
    if cpu_status_timer is None:
        cpu_status_timer = Timer(interval, background_timer_stuff, [socketio, interval, "cpu.status.res", CPUProfiler(server).get_status])
        cpu_status_timer.start()
    emit("cpu.status.res", CPUProfiler(server).get_status())

cpu_avg_timer = None
@cpu_blueprint.on('cpu.avgload.req')
def get_avg_load(request):
    server = request['server']
    interval = request['interval']
    socketio = cpu_blueprint.get_io()
    global cpu_avg_timer
    if cpu_avg_timer is None:
        cpu_avg_timer = Timer(interval, background_timer_stuff, [socketio, interval, "cpu.avgload.res", CPUProfiler(server).get_average_load])
        cpu_avg_timer.start()
    emit("cpu.avgload.res", CPUProfiler(server).get_average_load())

cpu_top_timer = None
@cpu_blueprint.on('cpu.top.req')
def get_top(request):
    server = request['server']
    interval = request['interval']
    socketio = cpu_blueprint.get_io()
    global cpu_top_timer
    if cpu_top_timer is None:
        cpu_top_timer = Timer(interval, background_timer_stuff, [socketio, interval, "cpu.top.res", CPUProfiler(server).getTopOutput])
        cpu_top_timer.start()
    emit("cpu.top.res", CPUProfiler(server).getTopOutput())
