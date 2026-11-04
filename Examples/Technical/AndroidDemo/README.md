# Android native AdaUI example

From the AdaExamples root, set ADAENGINE_ROOT to a compatible engine checkout:

```sh
python3 "$ADAENGINE_ROOT/Tools/Android/android.py" run --package Examples/Technical/AndroidDemo --product AndroidDemo
```

Use the engine's documented Swift Android SDK, Swan/Dawn, NDK and adb setup.
The Swift package exports a dynamic library and bundles its resource fixture.
See the [Android guide](https://github.com/AdaEngine/Ada/blob/main/Tools/Android/README.md).
