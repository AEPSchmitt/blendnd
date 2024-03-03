# blendnd
D&amp;D plugin for blender. Join a room to synchronize object transforms with other people in the same room.

## Prerequisites
```
pip install "python-socketio[client]"
```

## Installation
0. Install **socketio** and ensure Blender has access to the package (this may be an issue, depending on how you installed Blender)
1. Download **blendnd-pluging.zip**
2. Open Blender
3. Go to **Edit > Preferences > Add-ons** and select **Install**
4. Select the downloaded **blendnd-pluging.zip**
5. Enable the add-on by ticking the box
6. Open the same blender file as the rest of your group (a scenario created by your DM)
7. Open the **D&D** plugin menu (right side of the Viewport - you may need to click the little arrow next to the XYZ gizmo)
8. Enter the same room code as your D&D group and click **connect**
9. Play!

## Disclaimer
This is still very much an early prototype. No sharing of models between connected players, only support of simple transforms of existing models is currently implemented.
Only tested on Linux.

## Known issues
Multiple models with the same name in your scene cause problems.
Setting up your Python environment to access socketio may take more steps if you installed Blender through Steam.
