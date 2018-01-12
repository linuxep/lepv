from flask_socketio import emit
from app.modules.lepd.LepDClient import LepDClient
from app.modules.utils.socketIOBlueprint import SocketIOBlueprint

util_blueprint = SocketIOBlueprint('')


@util_blueprint.on('lepd.ping')
def ping_lepd_server(request):

    server = request['server']
    print('received ping: ' + server)

    client = LepDClient(server=server)

    ping_result = client.ping()

    if ping_result:
        emit('lepd.ping.succeeded', {})
    else:
        emit('lepd.ping.failed', {})