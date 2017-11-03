from modules.utils.socketIOBlueprint import SocketIOBlueprint
from flask_socketio import emit
from modules.profilers.cpu.CPUProfiler import CPUProfiler

cpu_blueprint = SocketIOBlueprint('')


@cpu_blueprint.on('cpu.stat.req')
def get_cpu_stat(request):
    print('received cpu.stat.req: ' + request['server'])

    server = request['server']
    profiler = CPUProfiler(server)
    data = profiler.get_stat()

    emit('cpu.stat.res',  data)


@cpu_blueprint.on('cpu.status.req')
def get_cpu_status(request):
    print('received cpu.status.req: ' + request['server'])

    server = request['server']
    profiler = CPUProfiler(server)
    data = profiler.getStatus()

    emit('cpu.status.res',  data)


@cpu_blueprint.on('cpu.avgload.req')
def get_avg_load(request):
    print('received cpu.avgload.req: ' + request['server'])

    server = request['server']
    profiler = CPUProfiler(server)
    data = profiler.get_average_load()

    emit('cpu.avgload.res',  data)


@cpu_blueprint.on('cpu.top.req')
def get_top(request):
    print('received cpu.top.req: ' + request['server'])

    server = request['server']
    profiler = CPUProfiler(server)
    data = profiler.getTopOutput()

    emit('cpu.top.res',  data)
