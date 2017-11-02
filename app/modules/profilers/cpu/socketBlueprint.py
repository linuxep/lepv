from modules.io_blueprint import SocketIOBlueprint
from flask_socketio import emit
from modules.profilers.cpu.CPUProfiler import CPUProfiler

cpu_blueprint = SocketIOBlueprint('')


@cpu_blueprint.on('cpu.stat.req')
def get_avg_load(request):
    print('received cpu.stat.req: ' + request['server'])

    server = request['server']
    profiler = CPUProfiler(server)
    data = profiler.get_stat()

    emit('cpu.stat.res',  data)

