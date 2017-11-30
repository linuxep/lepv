from flask import Flask, render_template
from flask_socketio import SocketIO

from modules.utils.localization import Languages
from modules.utils.simpleJson import MyJSONEncoder

app = Flask(__name__)
app.json_encoder = MyJSONEncoder

socketio = SocketIO(app)


#  CPU ---------------
from modules.profilers.cpu.views import cpuAPI
app.register_blueprint(cpuAPI)

from modules.profilers.cpu.sockets import cpu_blueprint
cpu_blueprint.init_io(socketio)


#  IO ----------------
from modules.profilers.io.views import ioAPI
app.register_blueprint(ioAPI)

from modules.profilers.io.sockets import io_blueprint
io_blueprint.init_io(socketio)


#  Memory ------------
from modules.profilers.memory.views import memoryAPI
app.register_blueprint(memoryAPI)

from modules.profilers.memory.sockets import memory_blueprint
memory_blueprint.init_io(socketio)


#  Perf  -------------
from modules.profilers.perf.views import perfAPI
app.register_blueprint(perfAPI)

from modules.profilers.perf.sockets import perf_blueprint
perf_blueprint.init_io(socketio)


#  Utils  ------------
from modules.utils.views import utilAPI
app.register_blueprint(utilAPI)


@app.route('/')
def index():
    languages = Languages().getLanguagePackForCN()
    return render_template("index.html", languages=languages)


@app.route('/swagger')
def swagger():
    return render_template("swagger.html")


@app.route('/test')
def test():
    languages = Languages().getLanguagePackForCN()
    return render_template("test.html", languages=languages)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8889)
