from flask_socketio import emit
from modules.lepd.LepDClient import LepDClient
from modules.utils.socketIOBlueprint import SocketIOBlueprint

util_blueprint = SocketIOBlueprint('')


@util_blueprint.on('ping')
def ping_lepd_server(request):

    server = request['server']
    print('received ping: ' + server)

    client = LepDClient(server=server)

    data = {
        'connected': client.ping()
    }

    emit('pong', data)