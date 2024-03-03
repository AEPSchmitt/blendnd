# blendnd
D&amp;D plugin for blender. Synchronize object transforms in a scene between multiple players.

## Prerequisites
```
pip install "python-socketio[client]"
```

## Installation
0. First install **socketio** and ensure Blender has access to the package (this may be an issue, depending on how you installed Blender).
1. Download **blendnd-pluging.zip**
2. Open Blender.
3. Go to **Edit > Preferences > Add-ons** and select **Install**
4. Select the downloaded **blendnd-pluging.zip**.
5. Enable the add-on by ticking the box
6. Open the same blender file as the rest of your group (a scenario created by your DM)
7. Open the **D&D** plugin menu (right side of the Viewport. You may need to click the little arrow next to the XYZ gizmo)
8. Enter the same room code as your D&D group and click **connect**

## Disclaimer
This is still very much an early prototype. No sharing of models between connected players, only support of simple transforms of existing models is currently implemented.
Obly tested on Linux.

## Known issues
Multiple models with the same name in your scene cause problems.
