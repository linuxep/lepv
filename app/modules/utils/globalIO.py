def _init():
    global _global_io
    _global_io = {}

def set_io(io):
    _global_io["io"] = io

def get_io():
    return _global_io["io"]