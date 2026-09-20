# Unfold the World

An AdaScript sample for AdaEditor's Foldable Preview. One scene keeps running while a
second display region reveals an interactive mission map.

## Play in AdaEditor

1. Open this folder as a project and open `Assets/Scenes/Main.ascn`.
2. Click the scene's **Play** control.
3. Choose **Display → Foldable Preview**, then **Expanded**.
4. Tap the orange airlock on the map. The gate slides away and the drone continues to
   the dock.
5. Switch to **Compact**, then **Expanded**. The gate and drone retain their state.

**Fit** fits the neutral profile to the editor viewport; **1:1** displays its logical
point dimensions. The sample profile is 400 × 640 when compact and 820 × 640 when
expanded, with a 20-point excluded gap.

## Scene and UI

The Airlock entity has a `CompanionPanel` that references `@res://UI/Map.ui`. Its
persisted `scriptBindings` connect UI input to exported fields in the `unfold.gate`
script. The game loop applies changes, moves the gate, and publishes new UI snapshots.

The project uses the `DisplayLayout` AdaScript resource to read the current layout:

```swift
@res var display: DisplayLayout;

func update(context) {
    if (display.isExpanded) {
        posture = "EXPANDED / CONNECTED";
    } else {
        posture = "COMPACT";
    }
}
```

## Boundaries

This sample simulates layout regions. It does not read a hardware hinge sensor or
render two independent cameras. One scene runtime owns simulation while the additional
panel is rendered with AdaUI. Play changes do not modify the saved scene.
