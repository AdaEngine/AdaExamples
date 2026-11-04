# Navigation playground

From the AdaExamples root:

```sh
swift run --package-path Examples/Technical/Navigation NavigationDemo
swift run --package-path Examples/Technical/Navigation NavigationDemo --validate
swift run --package-path Examples/Technical/Navigation NavigationDemo --validate-script
```

The robot patrols goals using the bundled NavigationRobot.ada. Click to choose a
manual destination, rebake the navmesh, or resume the patrol. `--capture <path>`
uses the actual native renderer and checks picking. For Windows set ADAENGINE_ROOT
to an engine checkout, then use `Examples/Technical/Navigation/script/run_windows.ps1`;
`-ValidateScript` selects headless script validation and `-CapturePath` saves a frame.
The launcher prepares Windows Gravity/Tint from the selected engine's scripts.

See the [navigation guide](https://github.com/AdaEngine/Ada/blob/main/Sources/AdaNavigation/AdaNavigation.docc/AdaNavigation.md).
