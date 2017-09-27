from flask import Flask, render_template

from app.modules.language.Languages import Languages
from app.modules.utils.simpleJson import MyJSONEncoder

app = Flask(__name__)
app.json_encoder = MyJSONEncoder

@app.route('/')
def index():
    languages = Languages().getLanguagePackForCN()
    return render_template("index.html", languages = languages)


# CPU
from app.modules.cpu.views import cpuAPI
app.register_blueprint(cpuAPI)


# IO
from app.modules.io.views import ioAPI
app.register_blueprint(ioAPI)


# Memory
from app.modules.memory.views import memoryAPI
app.register_blueprint(memoryAPI)


# Perf
from app.modules.perf.views import perfAPI
app.register_blueprint(perfAPI)


# Util
from app.modules.utils.views import utilAPI
app.register_blueprint(utilAPI)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8889)
