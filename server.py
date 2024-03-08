import socketio
import eventlet
import time

IP = "localhost"
PORT = 1337

# Create a new Socket.IO server
sio = socketio.Server(cors_allowed_origins="*")
room_user_mapping = {}

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
    room = data['room_id']
    username = data['name']
    sio.enter_room(sid, room)

    # Add user to the room_user_mapping with username
    if room not in room_user_mapping:
        room_user_mapping[room] = {}
    room_user_mapping[room][sid] = username

    # Broadcast the updated user list to all clients in the room
    sio.emit('user_list', list(room_user_mapping[room].values()), room=room)

@sio.event
def change_name(sid, data):
    print(f"User {sid} changing name to {data['name']}")
    sio.emit('namechange', {'id' : sid, 'name' : data['name']}, room=data['room_id'], skip_sid=sid)

@sio.event
def leave(sid, data):
    print(f"User {sid} left room {data['room_id']}")
    sio.leave_room(sid, data['room_id'])
    for room, users in room_user_mapping.items():
        if sid in users:
            room_user_mapping[room].pop(sid)
            sio.emit('user_list', list(users), room=room)

# Define an event handler for the 'disconnect' event
@sio.event
def disconnect(sid):
    print(f"Client disconnected: {sid}")
    for room, users in room_user_mapping.items():
        if sid in users:
            room_user_mapping[room].pop(sid)
            sio.emit('user_list', list(users), room=room)

# Create the application instance
app = socketio.WSGIApp(sio)

# Run the server
if __name__ == "__main__":
    # Use eventlet as the web server
    eventlet.wsgi.server(eventlet.listen((IP, PORT)), app)