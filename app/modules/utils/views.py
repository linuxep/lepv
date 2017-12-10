
"""Module for utilities"""


from flask import Blueprint, jsonify

from modules.lepd.LepDClient import LepDClient
from modules.utils.methodMap import MethodMap

utilAPI = Blueprint('utilAPI', __name__, url_prefix='/api')


@utilAPI.route('/ping/<server>', methods=['GET'])
def ping(server):

    client = LepDClient(server=server)

    data = {}
    data['connected'] = client.ping()

    return jsonify(data)


@utilAPI.route('/command/<command>/<server>', methods=['GET'])
def runRawCommand(command, server):

    client = LepDClient(server=server)

    data = client.sendRequest(command)
    data['splitted'] = client.split_to_lines(data['result'])

    return jsonify(data)
