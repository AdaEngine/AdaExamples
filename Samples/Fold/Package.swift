// swift-tools-version: 6.2
import PackageDescription

let package = Package(
    name: "Fold",
    platforms: [.macOS(.v15)],
    products: [.executable(name: "Fold", targets: ["Fold"])],
    dependencies: [
        .package(
            url: "https://github.com/AdaEngine/AdaEngine.git",
            revision: "810a744af3b3db3f31f54530ce3edebd280c7374"
        )
    ],
    targets: [
        .target(
            name: "FoldGame",
            dependencies: [.product(name: "AdaEngine", package: "AdaEngine")],
            resources: [.copy("../../Assets")],
            plugins: [.plugin(name: "AdaScriptBuildPlugin", package: "AdaEngine")]
        ),
        .executableTarget(name: "Fold", dependencies: ["FoldGame", .product(name: "AdaEngine", package: "AdaEngine")]),
        .testTarget(name: "FoldGameTests", dependencies: ["FoldGame"])
    ]
)
