# Skeletal Garden — AdaScript

A portable AdaScript project for Ada Studio. Open this folder in Studio and press
Run (macOS). There is no Swift package or game-specific Swift host to build.
This version requires Studio built with `ModelAnimationPlayback3DComponent`,
`CameraCollision3DComponent` and portable model LOD support; older Studio releases
will need an update.

The original 48×48 m garden is preserved: 65 trees, 42 rocks, 193 grass tufts,
60 terrain chunks with three stitched LODs, the plaza, pond, gateway, jumping
terraces and lookout. The two independent CC0 RobotExpressive models retain GPU
skinning, animated shadows and mesh LODs. The controlled robot evaluates its pose
every frame; the reference robot uses animation LOD and plays Walk at 0.65 speed.
Original textured props and baked IBL are unchanged.

- WASD: camera-relative walking; Shift: run (1.65 / 3.3 m/s).
- Space: jump on a press edge. R: reset position and accumulated controller motion.
- Left mouse drag: orbit. Q/E: zoom. The native sphere sweep retracts the camera
  around geometry and smoothly restores its distance.
- 1: sunlight shadows; 2: SSAO; 3: FXAA; 4: one/three cascades.
- 5: frustum culling; 6: mesh LOD; 7: MetalFX Temporal (supported Metal devices).
- 8: local lighting; 9: local shadows; 0: GPU visibility (supported backends).

`Sources/Garden.ada` owns movement and Idle/Walk/Run/Jump/Fall/Land decisions,
including hysteresis, cycle phase synchronization, cross-fades and speed matching
from collision-resolved motion. `Sources/Camera.ada` owns orbit, zoom and follow
smoothing. `Sources/Lighting.ada` owns quality switches. All keys are declared as
input actions in `.ada/project.json`.

`Assets/Scenes/Main.ascn` owns the complete world, model references, static
colliders, controller configuration, lights and camera environment. GLB terrain
chunks share the same height samples and triangle split as the full-resolution
8192-triangle collider. Native engine components implement physics, animation
playback, collision queries and rendering; they contain no garden rules.

Regenerate authored terrain/landmark assets and scene offline:

```sh
python3 SourceAssets/bake_scene.py
```

Model and IBL provenance remains in [SourceAssets/ASSETS.md](SourceAssets/ASSETS.md).
The previous Swift renderer benchmark reports are retained in
`SourceAssets/SwiftValidation` as historical evidence. Their executable flags,
crowd/capture modes and timing measurements do not describe this AdaScript
project. Use Studio's normal Run/export workflows for the new project.

Validate scene geometry (JSON or Studio-saved YAML):

```sh
python3 -m pip install -r Tests/requirements.txt
python3 -B -m unittest discover -s Tests -v
```
