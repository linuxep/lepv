from flask_socketio import emit


def process_socket_request(request, socket_req_message_key, profiler_method):

    server = request['server']
    print('received ' + socket_req_message_key + ': ' + server)

    data = profiler_method()

    if "request_id" in request:
        data['response_id'] = request['request_id']

    if "request_time" in request:
        data['request_time'] = request['request_time']

    socket_res_message_key = socket_req_message_key.replace(".req", ".res")

    emit(socket_res_message_key,  data)

