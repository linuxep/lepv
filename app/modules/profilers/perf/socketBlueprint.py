from modules.io_blueprint import SocketIOBlueprint
from flask_socketio import emit
from modules.profilers.perf.PerfProfiler import PerfProfiler

perf_blueprint = SocketIOBlueprint('')


@perf_blueprint.on('perf.cpuclock.req')
def get_perf_cpu_clock(request):
    print('received perf.cpuclock.req: ' + request['server'])

    server = request['server']
    profiler = PerfProfiler(server)
    data = profiler.getPerfCpuClock()

    emit('perf.cpuclock.res',  data)
