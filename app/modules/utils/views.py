
"""Module for utilities"""


from flask import Blueprint, jsonify

from modules.lepd.LepDClient import LepDClient
from modules.methodMap.MethodMap import MethodMap

utilAPI = Blueprint('utilAPI', __name__, url_prefix='/api/util')


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
    return jsonify(data)


@utilAPI.route('/command/mapping', methods=['GET'])
def getCommandMapping():

    methodMap = MethodMap()
    return jsonify(methodMap.getMap())