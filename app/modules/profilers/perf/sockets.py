from modules.utils.socketIOBlueprint import SocketIOBlueprint
from modules.profilers.perf.PerfProfiler import PerfProfiler
from modules.utils.soketProcessor import process_socket_request

perf_blueprint = SocketIOBlueprint('')


@perf_blueprint.on('perf.cpuclock.req')
def get_perf_cpu_clock(request):
    server = request['server']
    process_socket_request(request, 'perf.cpuclock.req', PerfProfiler(server).get_perf_cpu_clock)