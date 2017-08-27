from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
   return render_template("index.html", server = "www.linuxxueyuan.com")


@app.route('/command/<cmd>')
def sendRawCommand(cmd):
   return 'Sending raw command: %s!' % cmd


@app.route('/cpu/count/<server>')
def getCpuCount(server):
   return 'Getting CPU processor count for server: %s!' % server


if __name__ == '__main__':
    app.run()
