from modules.io_blueprint import SocketIOBlueprint
from flask_socketio import emit
from modules.profilers.io.IOProfiler import IOProfiler

io_blueprint = SocketIOBlueprint('')


@io_blueprint.on('io.status.req')
def get_io_status(request):
    print('received io.status.req: ' + request['server'])

    server = request['server']
    profiler = IOProfiler(server)
    data = profiler.get_status()

    emit('io.status.res',  data)


@io_blueprint.on('io.top.req')
def get_io_top(request):
    print('received io.top.req: ' + request['server'])

    server = request['server']
    profiler = IOProfiler(server)
    data = profiler.get_io_top()

    emit('io.top.res',  data)