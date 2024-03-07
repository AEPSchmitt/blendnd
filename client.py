import bpy
import socketio

from mathutils import Vector
from bpy.props import (StringProperty,
                        PointerProperty)


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

class Config:
    ADDON_NAME = 'dnd_plugin'
    GITHUB_REPOSITORY_URL = 'https://github.com/AEPSchmitt/blendnd'
    GITHUB_REPOSITORY_API_URL = 'https://api.github.com/repos/AEPSchmitt/blendnd'

sio = socketio.Client()
@sio.event
def connect():
    bpy.utils.register_class(ActionPanel)
    print("Connected to the server")

# Define an event handler for the 'message' event
@sio.event
def message(data):
    print(f"Message from the server: {data}")
    #bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 0))
    #bpy.context.view_layer.update()

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
    bpy.utils.unregister_class(ActionPanel)
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
    room_id: StringProperty(
        name="",
        default="( room key )",
        description="Enter room name"
    )
    player_name = StringProperty(
        name="",
        default="( choose name )",
        description="Enter your name"
    )
    
class ConnectionPanel(bpy.types.Panel):
    bl_label = "ROOM"
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
        row.operator("server.custom", icon="RNA", text="Settings")
        
        
class ActionPanel(bpy.types.Panel):
    bl_label = "Actions"
    bl_idname = "dnd_act"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "D&D"
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(icon="ORIENTATION_CURSOR", text="CONNECTED")
        #row.operator("server.ping")
        
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
        row.label(icon="RNA", text="Host:")
        row.prop(login, "server_ip")
    
class ConnectServer(bpy.types.Operator):
    bl_idname = "server.start"
    bl_label = "connect"
    bl_description="Connect to room"
    
    def execute(self, context):
        login = get_dnd_login_properties()
        if sio.connected:
            sio.emit('leave', { 'room_id': login.room_id})
        else:
            sio.connect('ws://'+login.server_ip+':1337')
        sio.emit('join', { 'room_id': login.room_id})
        on_depsgraph_update.operator = None
        bpy.app.handlers.depsgraph_update_post.append(on_depsgraph_update)
        return {'FINISHED'}

class OpenCustomIP(bpy.types.Operator):
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


class PlayerPanel(bpy.types.Panel):
    bl_label = "Players"
    bl_idname = "player.list"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "D&D"
    
    def draw(self, context):
        layout = self.layout

    def add_player(self, name):
        layout = self.layout
        row = layout.row()
        row.operator(text=name)


classes = (
    ConnectServer,
    DisconnectServer,
    OpenCustomIP,
    PingServer,
    DNDLoginProps,
    ConnectionPanel,
    #ActionPanel
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.WindowManager.dnd_properties = PointerProperty(type=DNDLoginProps)
        
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
    bpy.utils.unregister_class(ActionPanel)
    bpy.utils.unregister_class(IPanel)
        
if __name__ == "__main__":
    register()