from app.modules.lepd.LepDClient import LepDClient

LepdClient = LepDClient('www.linuxxueyuan.com', config='debug')


def NewLepdClient(server):
    global LepdClient
    LepdClient = LepDClient(server, config='debug')
