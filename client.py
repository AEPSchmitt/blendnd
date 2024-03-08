import bpy
import socketio

from mathutils import Vector
from bpy.props import (StringProperty,
                        PointerProperty,
                        EnumProperty)


bl_info = {
    'name': 'D&D Plugin',
    'description': 'Use blenders Object Mode to control a scene shared by the connected players',
    'author': 'AEPSchmitt',
    'license': 'APACHE2',
    'deps': '',
    'version': (1, 0),
    "blender": (2, 80, 0),
    'location': 'View3D > Tools > D&D',
    'warning': '',
    'wiki_url': 'https://github.com/AEPSchmitt/blendnd',
    'tracker_url': 'https://github.com/AEPSchmitt/blendnd/issues',
    'link': 'https://github.com/AEPSchmitt/blendnd',
    'support': 'COMMUNITY',
    'category': '3D View'
}

PLUGIN_VERSION = str(bl_info['version']).strip('() ').replace(',', '.')
is_plugin_enabled = False

group = []

class Config:
    ADDON_NAME = 'dnd_plugin'
    GITHUB_REPOSITORY_URL = 'https://github.com/AEPSchmitt/blendnd'
    GITHUB_REPOSITORY_API_URL = 'https://api.github.com/repos/AEPSchmitt/blendnd'

sio = socketio.Client()
@sio.event
def connect():
    bpy.utils.register_class(RoomPanel)
    print("Connected to the server")

# Define an event handler for the 'message' event
@sio.event
def message(data):
    print(f"Message from the server: {data}")
    #bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 0))
    #bpy.context.view_layer.update()
    
@sio.event
def user_list(data):
    group.clear()
    i = 0
    for d in data:
        group.append(('test', d, 'player '+str(i)))
        i += 1
      
@sio.event
def player_joined(data):
    if data:
        group.append((data['id'], data['id'], "player"))

@sio.event
def player_left(data):
    if data:
        for i in group:
            if group[i][0] == data['id']:
                group.remove(group[i])
                break
        
@sio.event
def action(data):
    if data:
        target_obj = bpy.data.objects[data['id']]
        if target_obj:
            target_obj.location = string_to_vector(data['location'])
            target_obj.scale = string_to_vector(data['scale'])
            target_obj.rotation_euler = string_to_vector(data['rotation'])


# Define an event handler for the 'disconnect' event
@sio.event
def disconnect():
    bpy.utils.unregister_class(RoomPanel)
    print("Disconnected from the server")
    
# helpers
def vector_to_string(vector):
    return ",".join(map(str, vector))

def string_to_vector(string):
    components = list(map(float, string.split(',')))
    return Vector(components)

def transformEvent(obj, scene, operation):
    sio.emit('action', {
        'type' : operation.name,
        'room_id' : bpy.context.window_manager.dnd_properties.room_id,
        'id': obj.name,
        'location' : vector_to_string(obj.location),
        'scale' : vector_to_string(obj.scale),
        'rotation' : vector_to_string(obj.rotation_euler)
    })

def on_depsgraph_update(scene):
    depsgraph = bpy.context.evaluated_depsgraph_get()
    if on_depsgraph_update.operator is None:
        on_depsgraph_update.operator = bpy.context.active_operator
    for update in depsgraph.updates:
        if not update.is_updated_transform:
            continue
        if on_depsgraph_update.operator == bpy.context.active_operator:
            continue
        obj = bpy.context.active_object
        operation = bpy.context.active_operator
        transformEvent(obj, scene, operation)
        on_depsgraph_update.operator = None

def get_dnd_login_properties():
    return bpy.context.window_manager.dnd_properties

class DNDLoginProps(bpy.types.PropertyGroup):
    bl_idname = "config.id"
    server_ip: StringProperty(
        name="",
        default="146.185.158.78",
        description="Server IP"
    )
    server_port: StringProperty(
        name="",
        default="1337",
        description="Server port"
    )
    room_id: StringProperty(
        name="",
        default="( choose key )",
        description="Enter room name"
    )

def get_players(self, context):
    return group

def get_room_info():
    return bpy.context.window_manager.room_info

def player_chosen(self):
    print(self)
    
class RoomProps(bpy.types.PropertyGroup):
    bl_idname = "room.info"
    players : EnumProperty(
        name="",
        items=get_players,
        description="Players in room"
    )
    player_name : StringProperty(
        name="",
        default="Kaladin",
        description="Enter your name"
    )

def get_id():
    return sio.sid

class ConnectionPanel(bpy.types.Panel):
    bl_label = "D&D Rooms"
    bl_idname = "dnd.connect"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "D&D"
    
    def draw(self, context):
        layout = self.layout
        
        login = get_dnd_login_properties()
        
        row = layout.row()
        row.label(icon="KEYINGSET")
        row.prop(login, "room_id")
        
        row = layout.row()
        row.operator("server.start", icon="PLAY", text="Enter")
        
        row = layout.row()
        row.operator("server.stop", icon="CANCEL", text="Leave")
        
        row = layout.row()
        row.operator("server.custom", icon="MODIFIER", text="Settings")
        
        
        
class RoomPanel(bpy.types.Panel):
    bl_label = "Room"
    bl_idname = "dnd_act"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "D&D"
    
    def draw(self, context):
        room = get_room_info()
        
        layout = self.layout
        row = layout.row()
        row.label(text="Your name:")
        row = layout.row()
        row.prop(room, "player_name")
        row.operator("room.changename", text="change")
        #row.label(text="CONNECTED")
        #row.label(icon="ORIENTATION_CURSOR")
        
        
        row = layout.row()
        row.label(text="Players:")
        row = layout.row()
        row.prop(room, "players")
        #row.operator("server.ping")
        
        #row = layout.row()
        #row.label(text="Your ID:")
        #row.label(text=sio.sid)

class ChangeName(bpy.types.Operator):
    bl_idname = "room.changename"
    bl_label = "change name"
    bl_description="Change Name"
    
    def execute(self, context):
        login = get_dnd_login_properties()
        room = get_room_info()
        sio.emit('join', { 'room_id': login.room_id, 'name' : room.player_name})
        return {'FINISHED'}
    
class IPanel(bpy.types.Panel):
    bl_label = "Host"
    bl_idname = "dnd_ip"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "D&D"
    
    def draw(self, context):
        login = get_dnd_login_properties()
        layout = self.layout
        row = layout.row()
        row.label(icon="LIBRARY_DATA_DIRECT", text="IP:")
        row.prop(login, "server_ip")
        row = layout.row()
        row.label(icon="SNAP_FACE_NEAREST", text="port:")
        row.prop(login, "server_port")
    
class ConnectServer(bpy.types.Operator):
    bl_idname = "server.start"
    bl_label = "connect"
    bl_description="Connect to room"
    
    def execute(self, context):
        login = get_dnd_login_properties()
        room = get_room_info()
        
        if sio.connected:
            sio.emit('leave', { 'room_id': login.room_id})
        else:
            sio.connect('ws://'+login.server_ip+':'+login.server_port)
        sio.emit('join', { 'room_id': login.room_id, 'name' : room.player_name})
        on_depsgraph_update.operator = None
        bpy.app.handlers.depsgraph_update_post.append(on_depsgraph_update)
        return {'FINISHED'}

class OpenSettings(bpy.types.Operator):
    bl_idname = "server.custom"
    bl_label = "settings"
    bl_description="Settings"
    
    def execute(self, context):
        bpy.utils.register_class(IPanel)
        return {'FINISHED'}

class DisconnectServer(bpy.types.Operator):
    bl_idname = "server.stop"
    bl_label = "disconnect"
    bl_description="Disconnect from room"
    
    def execute(self, context):
        sio.disconnect()
        group = []
        if on_depsgraph_update in bpy.app.handlers.depsgraph_update_post:
            bpy.app.handlers.depsgraph_update_post.remove(on_depsgraph_update)
        return {'FINISHED'}
    
class PingServer(bpy.types.Operator):
    bl_idname = "server.ping"
    bl_label = "ping"
    
    def execute(self, context):
        bpy.types.PlayerPanel.add_player(name='test')
        sio.send("ping")
        return {'FINISHED'}


classes = (
    ConnectServer,
    DisconnectServer,
    OpenSettings,
    ChangeName,
    PingServer,
    DNDLoginProps,
    RoomProps,
    ConnectionPanel
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.WindowManager.dnd_properties = PointerProperty(type=DNDLoginProps)
    bpy.types.WindowManager.room_info = PointerProperty(type=RoomProps)
        
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.utils.unregister_class(IPanel)
        
if __name__ == "__main__":
    register()