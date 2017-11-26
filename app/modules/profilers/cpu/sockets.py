from modules.utils.socketIOBlueprint import SocketIOBlueprint
from modules.profilers.cpu.CPUProfiler import CPUProfiler
from modules.utils.soketProcessor import process_socket_request

cpu_blueprint = SocketIOBlueprint('')


@cpu_blueprint.on('cpu.stat.req')
def get_cpu_stat(request):
    server = request['server']
    process_socket_request(request, 'cpu.stat.req', CPUProfiler(server).get_stat)


@cpu_blueprint.on('cpu.status.req')
def get_cpu_status(request):
    server = request['server']
    process_socket_request(request, 'cpu.status.req', CPUProfiler(server).getStatus)


@cpu_blueprint.on('cpu.avgload.req')
def get_avg_load(request):
    server = request['server']
    process_socket_request(request, 'cpu.avgload.req', CPUProfiler(server).get_average_load)


@cpu_blueprint.on('cpu.top.req')
def get_top(request):
    server = request['server']
    process_socket_request(request, 'cpu.top.req', CPUProfiler(server).getTopOutput)
