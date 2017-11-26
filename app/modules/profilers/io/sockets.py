from modules.utils.socketIOBlueprint import SocketIOBlueprint
from modules.profilers.io.IOProfiler import IOProfiler
from modules.utils.soketProcessor import process_socket_request

io_blueprint = SocketIOBlueprint('')


@io_blueprint.on('io.status.req')
def get_io_status(request):
    server = request['server']
    process_socket_request(request, 'io.status.req', IOProfiler(server).get_status)


@io_blueprint.on('io.top.req')
def get_io_top(request):
    server = request['server']
    process_socket_request(request, 'io.top.req', IOProfiler(server).get_io_top)
