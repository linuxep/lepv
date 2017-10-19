from modules.io_blueprint import IOBlueprint
from flask_socketio import emit
from modules.profilers.cpu.CPUProfiler import CPUProfiler

cpu_blueprint = IOBlueprint('')


@cpu_blueprint.on('cpu.avgload.request')
def get_avg_load(request):
    print('received cpu.avgload.request: ' + request['server'])

    server = request['server']
    profiler = CPUProfiler(server)
    data = profiler.get_average_load()

    emit('cpu.avgload.respond',  data)

