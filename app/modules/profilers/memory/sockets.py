from modules.utils.socketIOBlueprint import SocketIOBlueprint
from modules.profilers.memory.MemoryProfiler import MemoryProfiler
from modules.utils.soketProcessor import process_socket_request

memory_blueprint = SocketIOBlueprint('')


@memory_blueprint.on('memory.status.req')
def get_memory_status(request):
    server = request['server']
    process_socket_request(request, 'memory.status.req', MemoryProfiler(server).getStatus)


@memory_blueprint.on('memory.procrank.req')
def get_proc_rank(request):
    server = request['server']
    process_socket_request(request, 'memory.procrank.req', MemoryProfiler(server).getProcrank)