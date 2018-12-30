from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from app.modules.lepd.LepDClient import LepDClient

from app.modules.utils.localization import Languages
from app.modules.utils.simpleJson import MyJSONEncoder

app = Flask(__name__)
app.json_encoder = MyJSONEncoder

socketio = SocketIO(app, ping_timeout=3600)


@socketio.on('lepd.ping')
def ping_lepd_server(request):

    server = request['server']
    print('received ping: ' + server)

    client = LepDClient(server=server)

    ping_result = client.ping()

    if ping_result:
        emit('lepd.ping.succeeded', {})
    else:
        emit('lepd.ping.failed', {})

#  CPU ---------------
from app.modules.profilers.cpu.views import cpuAPI
app.register_blueprint(cpuAPI)

from app.modules.profilers.cpu.sockets import cpu_blueprint
cpu_blueprint.init_io(socketio)

#  IO ----------------
from app.modules.profilers.io.views import ioAPI
app.register_blueprint(ioAPI)

from app.modules.profilers.io.sockets import io_blueprint
io_blueprint.init_io(socketio)


#  Memory ------------
from app.modules.profilers.memory.views import memoryAPI
app.register_blueprint(memoryAPI)

from app.modules.profilers.memory.sockets import memory_blueprint
memory_blueprint.init_io(socketio)


#  Perf  -------------
from app.modules.profilers.perf.views import perfAPI
app.register_blueprint(perfAPI)

from app.modules.profilers.perf.sockets import perf_blueprint
perf_blueprint.init_io(socketio)


#  Utils  ------------
from app.modules.utils.views import utilAPI
app.register_blueprint(utilAPI)

# from app.modules.utils.sockets import util_blueprint
# util_blueprint.init_io(socketio)


@app.route('/')
def index():
    languages = Languages().getLanguagePackForCN()
    return render_template("index.html", languages=languages)

@app.route('/2')
def index2():
    languages = Languages().getLanguagePackForCN()
    return render_template("index2.html", languages=languages)


@app.route('/swagger')
def swagger():
    return render_template("swagger.html")


@app.route('/test')
def test():
    languages = Languages().getLanguagePackForCN()
    return render_template("test.html", languages=languages)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8889)
