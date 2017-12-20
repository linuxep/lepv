from modules.utils.socketIOBlueprint import SocketIOBlueprint
from modules.profilers.cpu.CPUProfiler import CPUProfiler
from modules.utils.soketProcessor import process_socket_request,background_timer_stuff
from flask_socketio import emit
import modules.utils.globalIO as gio 

cpu_blueprint = SocketIOBlueprint('')
socketio = gio.get_io()

cpu_stat_timer = None
@cpu_blueprint.on('cpu.stat.req')
def get_cpu_stat(request):
    server = request['server']
    interval = request['interval']
    global cpu_stat_timer
    if cpu_stat_timer is None:
        def background_stuff():
            while True:
                socketio.sleep(5)
                data = CPUProfiler(server).get_irq()
                socketio.emit("cpu.stat.res", data, broadcast=True)
        cpu_stat_timer = socketio.start_background_task(target=background_stuff)
    emit("cpu.stat.res", CPUProfiler(server).get_irq())
    
cpu_softirq_timer_running = False
@cpu_blueprint.on('cpu.softirq.req')
def get_cpu_softirq(request):
    server = request['server']
    interval = request['interval']
    global cpu_softirq_timer_running
    if cpu_softirq_timer_running == False:
        background_timer_stuff(socketio, interval, "cpu.softirq.req", CPUProfiler(server).get_softirq)
        cpu_softirq_timer_running = True
    emit("cpu.softirq.res", CPUProfiler(server).get_softirq())

cpu_status_timer_running = False
@cpu_blueprint.on('cpu.status.req')
def get_cpu_status(request):
    server = request['server']
    interval = request['interval']
    global cpu_status_timer_running
    if cpu_status_timer_running == False:
        background_timer_stuff(socketio, interval, "cpu.status.req", CPUProfiler(server).get_status)
        cpu_status_timer_running = True
    emit("cpu.status.res", CPUProfiler(server).get_status())

cpu_avg_timer_running = False
@cpu_blueprint.on('cpu.avgload.req')
def get_avg_load(request):
    server = request['server']
    interval = request['interval']
    global cpu_avg_timer_running
    if cpu_avg_timer_running == False:
        background_timer_stuff(socketio, interval, "cpu.avgload.req", CPUProfiler(server).get_average_load)
        cpu_avg_timer_running = True
    emit("cpu.avgload.res", CPUProfiler(server).get_average_load())

cpu_top_timer_running = False
@cpu_blueprint.on('cpu.top.req')
def get_top(request):
    server = request['server']
    interval = request['interval']
    global cpu_top_timer_running
    if cpu_top_timer_running == False:
        background_timer_stuff(socketio, interval, "cpu.top.req", CPUProfiler(server).getTopOutput)
        cpu_top_timer_running = True
    emit("cpu.top.res", CPUProfiler(server).getTopOutput())