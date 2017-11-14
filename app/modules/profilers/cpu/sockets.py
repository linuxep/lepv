from modules.utils.socketIOBlueprint import SocketIOBlueprint
from flask_socketio import emit
from modules.profilers.cpu.CPUProfiler import CPUProfiler

cpu_blueprint = SocketIOBlueprint('')

# @cpu_blueprint.on('cpu.count.req')
# def get_cpu_count(request):
#     print('received cpu.count.req: ' + request['server'])
#     server = request['server']
#     profiler = CPUProfiler(server)
#     data = profiler.getProcessorCount()
#
#     if "request_id" in request:
#         data['response_id'] = request['request_id']
#
#     emit('cpu.count.res',  data)

@cpu_blueprint.on('cpu.stat.req')
def get_cpu_stat(request):
    print('received cpu.stat.req: ' + request['server'])

    server = request['server']
    profiler = CPUProfiler(server)
    data = profiler.get_stat()

    if "request_id" in request:
        data['response_id'] = request['request_id']

    emit('cpu.stat.res',  data)


@cpu_blueprint.on('cpu.status.req')
def get_cpu_status(request):
    print('received cpu.status.req: ' + request['server'])

    server = request['server']
    profiler = CPUProfiler(server)
    data = profiler.getStatus()

    if "request_id" in request:
        data['response_id'] = request['request_id']

    emit('cpu.status.res',  data)


@cpu_blueprint.on('cpu.avgload.req')
def get_avg_load(request):
    print('received cpu.avgload.req: ' + request['server'])

    server = request['server']
    profiler = CPUProfiler(server)
    data = profiler.get_average_load()

    if "request_id" in request:
        data['response_id'] = request['request_id']

    emit('cpu.avgload.res',  data)


@cpu_blueprint.on('cpu.top.req')
def get_top(request):
    print('received cpu.top.req: ' + request['server'])

    server = request['server']
    profiler = CPUProfiler(server)
    data = profiler.getTopOutput()

    if "request_id" in request:
        data['response_id'] = request['request_id']

    emit('cpu.top.res',  data)
