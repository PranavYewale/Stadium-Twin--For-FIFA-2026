from flask_socketio import Namespace, emit

class StadiumNamespace(Namespace):
    def on_connect(self):
        print("Websocket client connected to Stadium Digital Twin")
        emit('connection_response', {'data': 'Connected to Digital Twin AI OS'})

    def on_disconnect(self):
        print("Websocket client disconnected")

    def on_ping_status(self, data):
        emit('pong_status', {'status': 'healthy'})
