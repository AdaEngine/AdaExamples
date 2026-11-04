# Movie recording example

From the AdaExamples root:

```sh
swift run --package-path Examples/Technical/MovieMaker MovieMakerDemo --write-movie Examples/Technical/MovieMaker/dist/demo.png --fixed-fps 60 --resolution 1280x720 --quit-after 180
```

This records native rendering and audio through the engine's MovieMaker. See the
[recording guide](https://github.com/AdaEngine/Ada/blob/main/Sources/AdaEngine/AdaEngine.docc/MovieMaker.md).
