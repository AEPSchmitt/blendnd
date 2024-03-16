import bpy
import socketio
import random as r
from mathutils import Vector
from bpy.props import (StringProperty,
                        PointerProperty,
                        EnumProperty,
                        IntProperty)


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
stuff = [("Bag of Holding", "Bag of Holding", "Bag of Holding")]
notes = [("Your Notes", "Your Notes", "Your Notes")]

class Config:
    ADDON_NAME = 'dnd_plugin'
    GITHUB_REPOSITORY_URL = 'https://github.com/AEPSchmitt/blendnd'
    GITHUB_REPOSITORY_API_URL = 'https://api.github.com/repos/AEPSchmitt/blendnd'

sio = socketio.Client()
@sio.event
def connect():
    bpy.utils.register_class(ROOM_PT_Panel)
    bpy.utils.register_class(CHARACTER_ATTRIBUTES_PT_Panel)
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
    bpy.utils.unregister_class(ROOM_PT_Panel)
    print("Disconnected from the server")
    
# helpers
def vector_to_string(vector):
    return ",".join(map(str, vector))

def string_to_vector(string):
    components = list(map(float, string.split(',')))
    return Vector(components)

def get_inventory(self, context):
    return stuff

def get_notes(self, context):
    return notes

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
    donate : StringProperty(
        name="",
        default="https://ko-fi.com/aepschmitt",
        description="Donation link"
    )

class CharacterAttributes(bpy.types.PropertyGroup):
    name: StringProperty(
        name="Name",
        description="Your Name",
        default="Gandalf"
    )
    race: StringProperty(
        name="Race",
        description="Your Race",
        default="Human"
    )
    class_: StringProperty(
        name="Class",
        description="Your Class",
        default="Wizard"
    )
    health: IntProperty(
        name="HP:",
        description="Current Health",
        default=10,
        min=0
    )
    armor_class: IntProperty(
        name="AC:",
        description="Armor Class",
        default=10,
        min=0
    )
    initiative: IntProperty(
        name="Init:",
        description="Initiative",
        default=10,
        min=0
    )
    lvl: IntProperty(
        name="LVL:",
        description="Level",
        default=1,
        min=0
    )
    xp: IntProperty(
        name="XP:",
        description="Experience Points",
        default=0,
        min=0
    )
    health_max: IntProperty(
        name="Max HP:",
        description="Max Health",
        default=20,
        min=0
    )
    strength: IntProperty(
        name="Strength",
        description="Your Strength",
        default=10,
        min=0
    )
    dexterity: IntProperty(
        name="Dexterity",
        description="Your Dexterity",
        default=10,
        min=0
    )
    constitution: IntProperty(
        name="Constitution",
        description="Your Constitution",
        default=10,
        min=0
    )
    intelligence: IntProperty(
        name="Intelligence",
        description="Your Intelligence",
        default=10,
        min=0
    )
    wisdom: IntProperty(
        name="Wisdom",
        description="Your Wisdom",
        default=10,
        min=0
    )
    charisma: IntProperty(
        name="Charisma",
        description="Your Charisma",
        default=10,
        min=0
    )
    inventory : EnumProperty(
        name="",
        items=get_inventory,
        description="Your stuff"
    )
    inventory_add : StringProperty(
        name="",
        default="new item",
        description="Your stuff"
    )
    notes : EnumProperty(
        name="",
        items=get_notes,
        description="Your private notes"
    )
    notes_add : StringProperty(
        name="",
        default="new note",
        description="Note to add"
    )

class DiceAttributes(bpy.types.PropertyGroup):
    count: IntProperty(
        name="",
        description="Amount of dice",
        default=1,
        min=1
    )
    sides: IntProperty(
        name="D",
        description="Dice sides",
        default=20,
        min=1
    )
    result: IntProperty(
        name="result:",
        description="Result of roll",
        default=0,
        min=0
    )

def get_dice():
    return bpy.context.window_manager.my_dice

def get_sheet():
    return bpy.context.window_manager.my_sheet

def get_players(self, context):
    return group

def get_room_info():
    return bpy.context.window_manager.room_info

def player_chosen(self):
    print(self)

class RollDice(bpy.types.Operator):
    bl_idname = "dice.roll"
    bl_label = "roll"
    bl_description="Roll Dice"
    
    def execute(self, context):
        dice = get_dice()
        print('rolling ', dice.count)
        print('side: ', dice.sides)
        res = 0
        for i in range(dice.count):
            res += r.randint(1, dice.sides)
        print(res)
        dice.result = res
        return {'FINISHED'}

class AddItem(bpy.types.Operator):
    bl_idname = "inventory.add"
    bl_label = "add item"
    bl_description="Add Item"
    
    def execute(self, context):
        my_sheet = get_sheet()
        new_item = my_sheet.inventory_add
        stuff.append((new_item, new_item, new_item))
        return {'FINISHED'}
    
class RemoveItem(bpy.types.Operator):
    bl_idname = "inventory.remove"
    bl_label = "remove item"
    bl_description="Remove Item"
    
    def execute(self, context):
        my_sheet = get_sheet()
        for item in stuff:
            if item[0] == my_sheet.inventory:
                stuff.remove(item)
                break
        return {'FINISHED'}
    
class AddNote(bpy.types.Operator):
    bl_idname = "notes.add"
    bl_label = "add note"
    bl_description="Add Note"
    
    def execute(self, context):
        my_sheet = get_sheet()
        new_notes = my_sheet.notes_add
        notes.append((new_notes, new_notes, new_notes))
        return {'FINISHED'}
    
class RemoveNote(bpy.types.Operator):
    bl_idname = "notes.remove"
    bl_label = "remove note"
    bl_description="Remove Note"
    
    def execute(self, context):
        my_sheet = get_sheet()
        for item in notes:
            if item[0] == my_sheet.notes:
                notes.remove(item)
                break
        return {'FINISHED'}

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

class CHARACTER_ATTRIBUTES_PT_Panel(bpy.types.Panel):
    bl_label = "Character Sheet"
    bl_idname = "CHARACTER_ATTRIBUTES_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "D&D"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        my_sheet = get_sheet()
        if my_sheet:
            attributes = my_sheet
            
            layout.row().prop(attributes, "name")
            layout.row().prop(attributes, "race")
            layout.row().prop(attributes, "class_")
        
            row = layout.row()
            row.prop(attributes, "health")
            row.prop(attributes, "health_max")
            
            row = layout.row()
            row.prop(attributes, "armor_class")
            row.prop(attributes, "initiative")
            
            row = layout.row()
            row.prop(attributes, "lvl")
            row.prop(attributes, "xp")
            
            layout.label(text="Stats", icon='TEXT')
            box = layout.box()
            col = box.column(align=True)
            col.prop(attributes, "strength")
            col.prop(attributes, "dexterity")
            col.prop(attributes, "constitution")
            col.prop(attributes, "intelligence")
            col.prop(attributes, "wisdom")
            col.prop(attributes, "charisma")
            
            layout.label(text="Inventory", icon='MOD_CLOTH')
            row = layout.row()
            row.prop(attributes, "inventory")
            row.operator("inventory.remove", text="remove")
            row = layout.row()
            row.prop(attributes, "inventory_add")
            row.operator("inventory.add", text="add")
            
            layout.label(text="Personal Notes", icon='HELP')
            row = layout.row()
            row.prop(attributes, "notes")
            row.operator("notes.remove", text="erase")
            row = layout.row()
            row.prop(attributes, "notes_add")
            row.operator("notes.add", text="add")

class CONNECTION_PT_Panel(bpy.types.Panel):
    bl_label = "D&D Rooms"
    bl_idname = "CONNECTION_PT_Panel"
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

        layout.label(text="Donate", icon='FUND')
        row = layout.row()
        row.operator("wm.url_open", text="ko-fi.com/aepschmitt").url = "https://ko-fi.com/aepschmitt"
        
class ROOM_PT_Panel(bpy.types.Panel):
    bl_label = "Room"
    bl_idname = "ROOM_PT_Panel"
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

class DICE_PT_Panel(bpy.types.Panel):
    bl_label = "Dice"
    bl_idname = "DICE_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "D&D"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        dice = get_dice()

        layout = self.layout
        row = layout.row()
        row.label(icon="MESH_ICOSPHERE")
        row.prop(dice, "count")
        row.prop(dice, "sides")
        
        row = layout.row()
        row.label(icon="FILE_3D")
        row.operator("dice.roll", text="roll")
        
        row = layout.row()
        row.prop(dice, "result")

class SERVER_PT_Panel(bpy.types.Panel):
    bl_label = "Host"
    bl_idname = "SERVER_PT_Panel"
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
        bpy.utils.register_class(SERVER_PT_Panel)
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
    CharacterAttributes,
    DiceAttributes,
    RollDice,
    OpenSettings,
    ChangeName,
    AddItem,
    RemoveItem,
    AddNote,
    RemoveNote,
    PingServer,
    DNDLoginProps,
    RoomProps,
    CONNECTION_PT_Panel,
    DICE_PT_Panel
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.WindowManager.dnd_properties = PointerProperty(type=DNDLoginProps)
    bpy.types.WindowManager.room_info = PointerProperty(type=RoomProps)
    bpy.types.WindowManager.my_sheet = PointerProperty(type=CharacterAttributes)
    bpy.types.WindowManager.my_dice = PointerProperty(type=DiceAttributes)
    
        
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
if __name__ == "__main__":
    register()