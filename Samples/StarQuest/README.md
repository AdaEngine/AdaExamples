# Star Quest

Star Quest is a complete AdaEngine UI sample. It combines a reusable `StarQuestGame`
library, a standalone `StarQuest` application, authored `.ui` documents, and a native
Swift UI implementation driven by the same model.

## Run

Open this folder in AdaEditor and run the **StarQuest** executable. For an embedded
preview, open `Sources/StarQuestGame/StarQuestView.swift`. The files under
`Assets/UI` can be edited in the UI Designer.

On macOS:

```sh
./script/build_and_run.sh
```

The script creates `dist/StarQuest.app` using an isolated build directory under
`/tmp`. Set `STARQUEST_BUILD_PATH` to use a different directory.

## Gameplay

- Start an adventure and collect five stars.
- Pause, resume, and return to the main menu without losing the current run.
- Complete the run to unlock the result screen, then start again.
- Change the background and panel width in Settings.
- Switch between the Swift and `.ui` implementations without resetting progress.

## Project structure

`StarQuestModel` owns state, actions, and bindings. Six `.ui` documents describe the
screens and receive actions through `UIBindingContext`. `NativeQuestScreen` implements
the same screens with AdaUI views. Textures come from Kenney UI Pack 2.0 and retain
their CC0 license in `Assets/Textures/License.txt`.

## Tests

```sh
swift test --scratch-path /tmp/starquest-build
```

The tests load the real UI documents and cover actions, repeated collection, pause,
resume, completion, and settings.
