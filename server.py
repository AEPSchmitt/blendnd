import socketio
import eventlet
import time

PORT = 1337

# Create a new Socket.IO server
sio = socketio.Server(cors_allowed_origins="*")

count = 0
# Define an event handler for the 'message' event
@sio.event
def message(sid, data):
    global count
    print(f"Message from {sid}: {data}")
    count += 1
    sio.emit('message', 'pong')

@sio.event
def move(sid, data):
    print(f"Move from {sid}: {data}")
    sio.emit('message', data)

@sio.event
def getplayers(sid, data):
    clients = sio.get_participants(room=data['room_id'])
    print(clients)
    sio.emit('players', clients)


@sio.event
def action(sid, data):
    print(f"Move from {sid}: {data}")
    print(f"Sending {data['type']} action to room: {data['room_id']}")
    sio.emit('action', data, room=data['room_id'], skip_sid=sid)

# Define an event handler for the 'connect' event
@sio.event
def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
def join(sid, data):
    print(f"User {sid} joining room {data['room_id']}")
    sio.enter_room(sid, data['room_id'])
    sio.emit('player_joined', {'id' : sid}, room=data['room_id'], skip_sid=sid)

@sio.event
def leave(sid, data):
    print(f"User {sid} left room {data['room_id']}")
    sio.leave_room(sid, data['room_id'])
    sio.emit('player_left', {'id' : sid}, room=data['room_id'], skip_sid=sid)

# Define an event handler for the 'disconnect' event
@sio.event
def disconnect(sid):
    print(f"Client disconnected: {sid}")

# Define a function to send a message to all connected clients
def send_message_to_all():
    message = "Server broadcast: Hello, clients!"
    print('broadcasting ping')
    sio.send(None, message)  # Broadcast to all connected clients

# Create the application instance
app = socketio.WSGIApp(sio)

# Run the server
if __name__ == "__main__":
    # Use eventlet as the web server
    eventlet.wsgi.server(eventlet.listen(("localhost", PORT)), app)