from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from modules.language.Languages import Languages
from modules.utils.simpleJson import MyJSONEncoder

app = Flask(__name__)
app.json_encoder = MyJSONEncoder

socketio = SocketIO(app)


@app.route('/')
def index():
    languages = Languages().getLanguagePackForCN()
    return render_template("index.html", languages=languages)


@app.route('/swagger')
def swagger():
    return render_template("swagger.html")


# CPU
from modules.profilers.cpu.views import cpuAPI
app.register_blueprint(cpuAPI)

from modules.profilers.cpu.socketBlueprint import cpu_blueprint
cpu_blueprint.init_io(socketio)


# IO
from modules.profilers.io.views import ioAPI
app.register_blueprint(ioAPI)


# Memory
from modules.profilers.memory.views import memoryAPI
app.register_blueprint(memoryAPI)


# Perf
from modules.profilers.perf.views import perfAPI
app.register_blueprint(perfAPI)


# Util
from modules.utils.views import utilAPI
app.register_blueprint(utilAPI)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8889)
