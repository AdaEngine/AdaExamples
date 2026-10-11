import { Garden } from "./Garden.ada";

@system(scheduler: "update", id: "garden.quality")
class GardenQualitySystem {
    @res var input: Input;
    @query(Environment3D, Camera) var cameras;
    @query(PointLightComponent) var points;
    @query(SpotLightComponent) var spots;

    func update(context) {
        for (var camera in cameras) {
            if (input.isActionJustPressed("Shadows")) camera.environment3D.shadowsEnabled = !camera.environment3D.shadowsEnabled;
            if (input.isActionJustPressed("AO")) camera.environment3D.ambientOcclusionEnabled = !camera.environment3D.ambientOcclusionEnabled;
            if (input.isActionJustPressed("AA")) camera.environment3D.fxaaEnabled = !camera.environment3D.fxaaEnabled;
            if (input.isActionJustPressed("Cascades")) {
                var count = 3;
                if (camera.environment3D.shadowCascadeCount == 3) count = 1;
                camera.environment3D.shadowCascadeCount = count;
            }
            if (input.isActionJustPressed("Culling")) camera.environment3D.frustumCullingEnabled = !camera.environment3D.frustumCullingEnabled;
            if (input.isActionJustPressed("LOD")) camera.environment3D.meshLODEnabled = !camera.environment3D.meshLODEnabled;
            if (input.isActionJustPressed("Temporal")) camera.camera.temporalUpscalingEnabled = !camera.camera.temporalUpscalingEnabled;
            if (input.isActionJustPressed("LocalShadows")) camera.environment3D.localShadowsEnabled = !camera.environment3D.localShadowsEnabled;
            if (input.isActionJustPressed("GPUVisibility")) camera.environment3D.gpuOcclusionEnabled = !camera.environment3D.gpuOcclusionEnabled;
        }
        // Keep each authored intensity rather than relying on entity order or demo IDs in the host.
        for (var point in points) {
            if (Garden.pointIntensities[point.id] == null) Garden.pointIntensities[point.id] = point.pointLightComponent.intensity;
        }
        for (var spot in spots) {
            if (Garden.spotIntensities[spot.id] == null) Garden.spotIntensities[spot.id] = spot.spotLightComponent.intensity;
        }
        if (input.isActionJustPressed("LocalLights")) {
            Garden.localLights = !Garden.localLights;
            for (var point in points) {
                var intensity = 0.0;
                if (Garden.localLights) intensity = Garden.pointIntensities[point.id];
                point.pointLightComponent.intensity = intensity;
            }
            for (var spot in spots) {
                var intensity = 0.0;
                if (Garden.localLights) intensity = Garden.spotIntensities[spot.id];
                spot.spotLightComponent.intensity = intensity;
            }
        }
    }
}
