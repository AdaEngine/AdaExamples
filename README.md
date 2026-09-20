# AdaExamples

Official examples and complete sample games for [AdaEngine](https://github.com/AdaEngine/AdaEngine).

## Repository layout

- `Examples` contains focused projects that demonstrate one engine feature.
- `Samples` contains complete, runnable games and larger reference projects.
- `Assets/Previews` contains the images used by catalog cards.
- `catalog.json` is the machine-readable catalog consumed by AdaEditor and the website.

Project templates intentionally live in a separate repository. This catalog contains
only examples and samples.

## Browse the catalog

Every catalog item has a stable ID, kind, project path, preview, and a controlled set
of tags. Tags cover language, rendering dimension, genre, engine features, and target
platforms. Run the validator after changing an item:

```sh
python3 scripts/validate_catalog.py
```

## Use a project

Download or clone this repository, open an item folder in AdaEditor, and follow its
README. Swift projects resolve the AdaEngine revision recorded in their
`Package.swift`; AdaScript-only projects open directly in AdaEditor.

## Contributing

Keep every project self-contained. Do not add local package paths, build output,
editor workspace state, or generated distribution bundles. Add a real preview under
`Assets/Previews` and describe the project in `catalog.json`.

All contributions must pass catalog validation. Swift samples are also built and
tested in CI.
