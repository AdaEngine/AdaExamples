// swift-tools-version: 6.2
import Foundation
import PackageDescription

let package = Package(
    name: "SponzaDemo",
    platforms: [.macOS(.v15), .iOS(.v18)],
    products: [.executable(name: "SponzaDemo", targets: ["SponzaDemo"])],
    dependencies: [
        .package(url: "https://github.com/AdaEngine/AdaEngine.git", revision: "b43d7e8f2f03e124a62b77499f7c2949a078dc27")
    ],
    targets: [
        .executableTarget(
            name: "SponzaDemo",
            dependencies: [
                "SponzaCamera",
                .product(name: "AdaEngine", package: "adaengine"),
                .product(name: "Math", package: "adaengine")
            ],
            path: ".",
            exclude: ["README.md", "Camera", "Tests"] + (FileManager.default.fileExists(atPath: "dist") ? ["dist"] : []),
            sources: [
                "SponzaDemo.swift",
                "SponzaDemoProfiler.swift",
                "SponzaLighting.swift",
                "SponzaStutterProfiler.swift",
                "SponzaWarmup.swift"
            ],
            resources: [.copy("Assets")],
            swiftSettings: [.enableUpcomingFeature("MemberImportVisibility"), .strictMemorySafety()]
        ),
        .target(name: "SponzaCamera", dependencies: [.product(name: "AdaTransform", package: "adaengine"), .product(name: "Math", package: "adaengine")], path: "Camera"),
        .testTarget(name: "SponzaDemoTests", dependencies: ["SponzaCamera", .product(name: "AdaTransform", package: "adaengine")], path: "Tests")
    ]
)
