# Technical examples

Developer studies and acceptance projects live here. Clone the repository and follow each README to run its SwiftPM package, XcodeGen
app or Studio project. These are not beginner recommendations or sample games;
not every technical tool is an editable Studio game project.

| Project | Focus |
| --- | --- |
| [Procedural Skeleton](ProceduralSkeleton/README.md) | Explicit AdaScript rig, vertex weights and a walk clip; precompiled builder and interpreted VM |
| [A2UIForm](A2UIForm/README.md) | Streamed agent forms and native control validation |
| [AndroidDemo](AndroidDemo/README.md) | Native Android window, input and resource smoke test |
| [LinuxSmoke](LinuxSmoke/README.md) | Linux X11/Vulkan window and input smoke test |
| [MovieMaker](MovieMaker/README.md) | Native frame and audio recording |
| [Navigation](Navigation/README.md) | Navmesh baking, patrol scripting and physics movement |
| [Physics2D](Physics2D/README.md) | Box2D queries, mechanisms, characters and large worlds |
| [SpineNative](SpineNative/README.md) | Native Spine rendering and MCP GPU capture |
| [SpinePreview](SpinePreview/README.md) | Headless Spine pose export and browser inspection |
| [Sponza](Sponza/README.md) | External-dataset renderer and lighting diagnostics |
| [SpriteInstancingValidation](SpriteInstancingValidation/README.md) | Portable GPU sprite readback validation |

This section is intentionally separate from `catalog.json`. Studio and website
catalogs consume only its `items`, and the release workflow packages only those
items. The catalog validator rejects `Examples/Technical/` paths to prevent an
accidental promotion into those feeds. Adding technical studies does not require a
new public catalog schema or changes to catalog consumers.

Commit the small assets needed to open a project. Keep build outputs, per-frame
captures, logs, workspace state and generated distributions ignored locally.

Swift packages pin a compatible engine revision. Their README commands run from the AdaExamples root. No engine checkout is required for normal SwiftPM dependency resolution; platform preparation tools, optional asset preparation and Windows capture overrides may require `ADAENGINE_ROOT`.

Developer checks: `python scripts/validate_catalog.py`, `python -m unittest discover -s scripts -p "test_*.py"` and `python scripts/validate_technical_packages.py --engine-root /path/to/Ada`. The last command checks package manifests, source/resource paths and declared engine products without downloading dependencies or proving a native app launch.
