"""Module for I/O related data parsing"""
__author__    = "Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

import datetime
import pprint
import re

from modules.lepd.LepDClient import LepDClient


class WebSocket:

    def __init__(self, socketio):
        self.socket = socketio

    def set_up_sockets(self):

        pass


if __name__ == '__main__':
    cpuSocket = WebSocket(None)

    cpuSocket.set_up_sockets()



