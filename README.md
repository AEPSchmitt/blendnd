# blendnd
D&amp;D plugin for blender. Synchronize object transforms in a scene between multiple players.

## Prerequisites
```
pip install "python-socketio[client]"
```

## Installation
0. First install **socketio** and ensure Blender has access to the package (this is only an issue if you have installed Blender through Steam).
1. Open the Blender scene created by your DM
2. Open **client.py** in Blenders scripting window
3. Run the script
4. Open the **D&D** plugin menu (right side of the Viewport. You may need to click the little arrow next to the XYZ gizmo)
5. Enter the same room code as your D&D group and click **connect**

## Disclaimer
This is still very much an early prototype. No sharing of models between connected players, only support of simple transforms of existing models is currently implemented.

## Known issues
Multiple models with the same name in your scene causes problems.
