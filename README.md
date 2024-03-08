# blendnd
D&amp;D plugin for blender.

![image](https://github.com/AEPSchmitt/blendnd/assets/9079958/e23dd6ad-b7e1-4d52-95b7-a88b0541b73c)


Join a room to synchronize object transforms with other people in the same room. Designed for virtual D&D but can also be used for other games. Download [**chess_test_scene.blend**](https://github.com/AEPSchmitt/blendnd/blob/main/chess_test_scene.blend) to try the addon with a game of chess.

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


   ![image](https://github.com/AEPSchmitt/blendnd/assets/9079958/730ab2c3-20bc-4898-819d-82e73d00fa20)
6. Open the same blender file as the rest of your group (a scenario created by your DM)
7. Open the **D&D** plugin menu (right side of the Viewport - you may need to click the little arrow next to the XYZ gizmo)
8. Enter the same room code as your D&D group and click **connect**
9. Play!

## Disclaimer
This is still very much an early prototype. Only transformations are shared with the room, not the addition or removal of models (yet). That means you will have to share the blender scene with all players beforehand.


Defaults to my socket managing server, but you can use **server.py** to set up your own and change the connection in the **Settings** menu.

## Known issues
Setting up your Python environment to access socketio may take more steps if you installed Blender through Steam.
