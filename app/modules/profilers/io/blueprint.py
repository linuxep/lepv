from modules.io_blueprint import SocketIOBlueprint
from flask_socketio import emit
from modules.profilers.io.IOProfiler import IOProfiler

io_blueprint = SocketIOBlueprint('')


@io_blueprint.on('io.status.request')
def get_io_status(request):
    print('received io.status.request: ' + request['server'])

    server = request['server']
    profiler = IOProfiler(server)
    data = profiler.get_status()

    emit('io.status.respond',  data)

