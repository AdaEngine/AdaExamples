// Game decisions live here; the scene owns models, lights, terrain and collision geometry.
class Garden {
    static var yaw = 0.45;
    static var elapsed = 0.0;
    static var localLights = true;
    static var locomotion = "Idle";
    static var facingYaw = 3.141592653589793;
    static var wasAirborne = false;
    static var landingTime = 0.0;
    static var pitch = 0.36;
    static var distance = 6.6;
    static var focus = [0.0, 1.15, 0.0];
    static var initialized = false;
    static var lastX = 0.0;
    static var lastY = 0.0;
    static var dragging = false;
    static var pointIntensities = [:];
    static var spotIntensities = [:];

    static func delta(context) { return Math.clamp(context.deltaTime, 0.0, 0.1); }
}

@system(scheduler: "update", id: "garden.input")
class GardenInputSystem {
    @res var input: Input;
    @query(CharacterController3DComponent, Transform) var players;

    func update(context) {
        Garden.elapsed += Garden.delta(context);
        var x = input.getActionStrength("MoveRight") - input.getActionStrength("MoveLeft");
        var z = input.getActionStrength("MoveForward") - input.getActionStrength("MoveBack");
        var direction = [x * Math.cos(Garden.yaw) - z * Math.sin(Garden.yaw), 0.0,
                         x * Math.sin(Garden.yaw) + z * Math.cos(Garden.yaw)];
        var speed = 1.65;
        if (input.isActionPressed("Run")) speed = 3.3;
        if (Math.length(direction) > 0.01) direction = Math.scaleVector(Math.normalize(direction), speed);
        for (var row in players) {
            row.characterController3DComponent.desiredVelocity = direction;
            if (input.isActionJustPressed("Jump")) row.characterController3DComponent.jumpRequested = true;
            if (input.isActionJustPressed("Reset") || row.transform.position[1] < -8.0) {
                row.transform.position = [-0.7, 0.1, 0.0];
                row.characterController3DComponent.desiredVelocity = [0.0, 0.0, 0.0];
                row.characterController3DComponent.resetMotion = true;
            }
        }
    }
}

// Fixed post-update observes collision-resolved velocity after the character controller.
@system(scheduler: "fixedPostUpdate", id: "garden.animation")
class GardenAnimationSystem {
    @query(CharacterController3DComponent, Transform, ModelAnimationPlayback3DComponent) var players;

    func update(context) {
        var dt = Garden.delta(context);
        for (var row in players) {
            var velocity = row.characterController3DComponent.velocity;
            var speed = Math.sqrt(velocity[0] * velocity[0] + velocity[2] * velocity[2]);
            var idleThreshold = 0.07;
            if (Garden.locomotion == "Idle") idleThreshold = 0.16;
            var runThreshold = 2.475;
            if (Garden.locomotion == "Run") runThreshold = 2.1;
            var clip = "Walk";
            if (speed < idleThreshold) clip = "Idle";
            else if (speed > runThreshold) clip = "Run";
            var grounded = row.characterController3DComponent.isGrounded;
            if (!grounded && Garden.elapsed > 0.15) {
                Garden.wasAirborne = true;
                Garden.landingTime = 0.0;
                clip = "Fall";
                if (velocity[1] > 0.15) clip = "Jump";
            } else if (grounded && Garden.wasAirborne) {
                Garden.wasAirborne = false;
                Garden.landingTime = 0.25;
            }
            if (grounded && Garden.landingTime > 0.0) {
                clip = "Land";
                Garden.landingTime = Math.max(0.0, Garden.landingTime - dt);
            }
            var air = clip == "Jump" || clip == "Fall" || clip == "Land";
            row.modelAnimationPlayback3DComponent.clip = clip;
            row.modelAnimationPlayback3DComponent.repeats = !air;
            row.modelAnimationPlayback3DComponent.synchronizePhase =
                (Garden.locomotion == "Walk" || Garden.locomotion == "Run") && (clip == "Walk" || clip == "Run");
            var transition = 0.22;
            if (air) transition = 0.08;
            row.modelAnimationPlayback3DComponent.transitionDuration = transition;
            var playbackSpeed = 1.0;
            if (!air && clip != "Idle") {
                var reference = 1.1;
                if (clip == "Run") reference = 2.2;
                playbackSpeed = Math.clamp(speed / reference, 0.25, 1.5);
            }
            row.modelAnimationPlayback3DComponent.speed = playbackSpeed;
            Garden.locomotion = clip;
            if (speed > 0.07) {
                var turn = (Math.atan2(velocity[0], velocity[2]) - Garden.facingYaw) % 6.283185307179586;
                if (turn > 3.141592653589793) turn -= 6.283185307179586;
                if (turn < -3.141592653589793) turn += 6.283185307179586;
                Garden.facingYaw += turn * (1.0 - Math.exp(-dt * 12.0));
                row.transform.rotation = [0.0, Math.sin(Garden.facingYaw / 2.0), 0.0, Math.cos(Garden.facingYaw / 2.0)];
            }
        }
    }
}
