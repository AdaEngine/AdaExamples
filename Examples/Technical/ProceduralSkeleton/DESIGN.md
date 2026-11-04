# Implementation map

- `Generators/Skeleton-Rig.ada`: complete interpreted recipe.
- `Generators/SkeletonRigRecipe.ada`: joints, semantic weights, two-bone IK, keys.
- `Generators/Skeleton.ada`, `author_recipe.py`: generated static geometry.
- `Assets/Scenes/Walk.ascn`: default native playback using Skeleton-AdaScript.glb.
- `Assets/Scenes/Showcase.ascn`: original static comparison.
- `script_rig.py`: optional developer harness; ADAENGINE_ROOT selects engine sources.
- `NativeRig/`, `native_rig.py`: previous Swift baseline for comparison only.
- `Validation/`: real importer/player acceptance and standalone harness adapter.
- `check_geometry.py`, `check_rig.py`: independent checks of actual GLB buffers.
- `rig_capture.py`: native playback capture; outputs remain ignored locally.

The example is not registered in catalog.json. The public validator rejects its
technical section, keeping Studio/website recommendations and release archives
unchanged. Units are meters, Y is up, and the character faces -Z.
