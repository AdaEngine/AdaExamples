# Sprite instancing validation

Separate QA app using production SpriteRenderSystem / SpriteDrawPass / shaders.
The same 640x360 GPU fixture covers stretch/fit/fill, sliced/tiled atlas regions,
flips, reflected/rotated transforms, anchors, alpha and ordered texture changes.
It compares readback pixels for five expanded and five instanced frames, with a
1200-sprite contiguous run. A PASS requires identical nonempty pixels and active
instancing. It reports backend, quads and draw count; no backend fallback counts as proof.

iOS, from this demo directory:

```sh
xcodegen generate --spec project.yml
```

Build and launch the scheme with `ADAENGINE_DISABLE_SWAN=1` in the host environment.
On iOS the visible PASS also writes `Documents/sprite-validation.json` in the QA
app's container, allowing a physical device result to be retrieved without relying
on launch success alone.

Browser, from the AdaExamples root (set `ADAENGINE_ROOT` to the engine checkout for Tint preparation):

```sh
python3 "$ADAENGINE_ROOT/script/ensure_tint.py"
ADAENGINE_WEB_EXPORT=1 swift package --package-path Examples/Technical/SpriteInstancingValidation --allow-writing-to-package-directory export-web \
  --product SpriteInstancingValidation --output dist/SpriteInstancingValidation \
  --scratch-path /tmp/ada-sprite-web-validation \
  --swift-sdk swift-6.3.2-RELEASE_wasm --debug
```

Use compatible Swan/Dawn; local development overrides are described in
[Tools/Tint](https://github.com/AdaEngine/Ada/blob/main/Tools/Tint/README.md). Serve the output over HTTP and inspect the
console `[SpriteValidation] PASS`. The canvas presents the validated GPU readback
image with a green border; failures log FAIL and show a red background. Known color
probes reject a blank frame even when both rendering modes produce equal bytes.

Recorded proof: macOS native WebGPU, actual WASM WebGPU, iPhone 17 Pro Simulator,
and physical iPad8,1 / iPadOS 26.5. Rendering correctness is verified; this app
provides no browser/mobile performance benchmark or Editor UI validation.
