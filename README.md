# blendnd
D&amp;D plugin for blender.

![dnd-addon](https://github.com/AEPSchmitt/blendnd/assets/9079958/bdcf92f9-5cb6-4995-9773-47b28ee30ad9)

Join a room to synchronize object transforms with other people in the same room.

## Prerequisites
```
pip install "python-socketio[client]"
```

## Installation
0. Install [**socketio**](https://python-socketio.readthedocs.io/en/stable/client.html) and ensure Blender has access to the package (this may be an issue, depending on how you installed Blender)
1. Download [**blendnd-plugin.zip**](https://github.com/AEPSchmitt/blendnd/blob/main/blendnd-plugin.zip) 
2. Open Blender
3. Go to **Edit > Preferences > Add-ons** and select **Install** ( [guide](https://www.youtube.com/watch?v=vYh1qh9y1MI) )
4. Navigate to and select **blendnd-pluging.zip**
5. Remember to enable the add-on after adding it
6. Open the same blender file as the rest of your group (a scenario created by your DM)
7. Open the **D&D** plugin menu (right side of the Viewport - you may need to click the little arrow next to the XYZ gizmo)
8. Enter the same room code as your D&D group and click **connect** (leave **IP** as is unless you want to use your own server)
9. Play!

## Disclaimer
This is still very much an early prototype. Only transformations are shared with the room, not the addition or removal of models (yet). That means you will have to share the blender scene with all players beforehand.

## Known issues
Setting up your Python environment to access socketio may take more steps if you installed Blender through Steam.
