# Technical examples

Developer studies and acceptance projects live here. Clone the repository and open
the desired project directly; these are not beginner recommendations or sample games.

| Project | Focus |
| --- | --- |
| [Procedural Skeleton](ProceduralSkeleton/README.md) | Explicit AdaScript rig, vertex weights and a walk clip; precompiled builder and interpreted VM |

This section is intentionally separate from `catalog.json`. Studio and website
catalogs consume only its `items`, and the release workflow packages only those
items. The catalog validator rejects `Examples/Technical/` paths to prevent an
accidental promotion into those feeds. Adding technical studies does not require a
new public catalog schema or changes to catalog consumers.

Commit the small assets needed to open a project. Keep build outputs, per-frame
captures, logs, workspace state and generated distributions ignored locally.
