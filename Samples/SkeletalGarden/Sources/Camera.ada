import { Garden } from "./Garden.ada";

@after(id: "garden.animation")
@system(scheduler: "fixedPostUpdate", id: "garden.camera")
class GardenCameraSystem {
    @res var input: Input;
    @query(CharacterController3DComponent, Transform) var players;
    @query(CameraCollision3DComponent) var cameras;

    func update(context) {
        var dt = Garden.delta(context);
        var target = [0.0, 1.15, 0.0];
        for (var player in players) target = Math.addVector(player.transform.position, [0.0, 1.15, 0.0]);
        var x = input.mouseX;
        var y = input.mouseY;
        var held = input.isActionPressed("Orbit");
        if (held && Garden.dragging) {
            Garden.yaw -= (x - Garden.lastX) * 0.008;
            Garden.pitch = Math.clamp(Garden.pitch + (y - Garden.lastY) * 0.006, 0.08, 1.1);
        }
        Garden.lastX = x;
        Garden.lastY = y;
        Garden.dragging = held;
        Garden.distance = Math.clamp(Garden.distance + (input.getActionStrength("ZoomOut") - input.getActionStrength("ZoomIn")) * dt * 5.0, 3.2, 12.0);
        if (!Garden.initialized || input.isActionJustPressed("Reset")) { Garden.focus = target; Garden.initialized = true; }
        Garden.focus = Math.lerpVector(Garden.focus, target, 1.0 - Math.exp(-dt * 12.0));
        var offset = Math.scaleVector([Math.sin(Garden.yaw) * Math.cos(Garden.pitch), Math.sin(Garden.pitch),
                                       -Math.cos(Garden.yaw) * Math.cos(Garden.pitch)], Garden.distance);
        for (var camera in cameras) {
            camera.cameraCollision3DComponent.origin = target;
            camera.cameraCollision3DComponent.destination = Math.addVector(Garden.focus, offset);
            camera.cameraCollision3DComponent.target = Garden.focus;
        }
    }
}
