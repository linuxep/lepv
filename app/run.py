from flask import Flask, render_template, jsonify

from app.profilers.CPUProfiler import CPUProfiler
from app.profilers.Languages import Languages


app = Flask(__name__)

@app.route('/')
def index():
    languages = Languages().getLanguagePackForCN()
    return render_template("index.html", languages = languages)


@app.route('/command/<cmd>')
def sendRawCommand(cmd):
    return 'Sending raw command: %s!' % cmd


@app.route('/cpu/count/<server>')
def getCpuCount(server):

    profiler = CPUProfiler(server)
    data = profiler.getProcessorCount()

    return jsonify(data)

if __name__ == '__main__':
    app.run()
