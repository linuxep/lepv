from app.modules.utils.socketIOBlueprint import SocketIOBlueprint
from app.modules.profilers.memory.MemoryProfiler import MemoryProfiler
from app.modules.utils.soketProcessor import process_socket_request, background_timer_stuff
from threading import Timer
from flask_socketio import emit

memory_blueprint = SocketIOBlueprint('')

memory_status_timer = None
@memory_blueprint.on('memory.status.req')
def get_memory_status(request):
    server = request['server']
    interval = request['interval']
    socketio = memory_blueprint.get_io()
    global memory_status_timer
    if memory_status_timer is None:
        memory_status_timer = Timer(interval, background_timer_stuff, [
            socketio, interval, "memory.status.res", MemoryProfiler(server).getStatus])
        memory_status_timer.start()
    emit("memory.status.res", MemoryProfiler(server).getStatus())
    # process_socket_request(request, 'memory.status.req', MemoryProfiler(server).getStatus)

memory_procrank_timer = None
@memory_blueprint.on('memory.procrank.req')
def get_proc_rank(request):
    server = request['server']
    interval = request['interval']
    socketio = memory_blueprint.get_io()
    global memory_procrank_timer
    if memory_procrank_timer is None:
        memory_procrank_timer = Timer(interval, background_timer_stuff, [
            socketio, interval, "memory.procrank.res", MemoryProfiler(server).getProcrank])
        memory_procrank_timer.start()
    emit("memory.procrank.res", MemoryProfiler(server).getProcrank())
    # process_socket_request(request, 'memory.procrank.req', MemoryProfiler(server).getProcrank)
