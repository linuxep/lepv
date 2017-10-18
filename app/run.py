import sys
from flask import Flask, render_template

from modules.language.Languages import Languages
from modules.utils.simpleJson import MyJSONEncoder

reload(sys)
sys.setdefaultencoding('utf8')
app = Flask(__name__)
app.json_encoder = MyJSONEncoder


@app.route('/')
def index():
    languages = Languages().getLanguagePackForCN()
    return render_template("index.html", languages=languages)


@app.route('/swagger')
def swagger():
    return render_template("swagger.html")


# CPU
from modules.cpu.views import cpuAPI
app.register_blueprint(cpuAPI)


# IO
from modules.io.views import ioAPI
app.register_blueprint(ioAPI)


# Memory
from modules.memory.views import memoryAPI
app.register_blueprint(memoryAPI)


# Perf
from modules.perf.views import perfAPI
app.register_blueprint(perfAPI)


# Util
from modules.utils.views import utilAPI
app.register_blueprint(utilAPI)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8889)
