// swift-tools-version: 6.2
import Foundation
import PackageDescription

let package = Package(
    name: "A2UIFormDemo",
    platforms: [.macOS(.v15), .iOS(.v18)],
    products: [.executable(name: "A2UIFormDemo", targets: ["A2UIFormDemo"])],
    dependencies: [
        .package(url: "https://github.com/AdaEngine/AdaEngine.git", revision: "b43d7e8f2f03e124a62b77499f7c2949a078dc27")
    ],
    targets: [
        .executableTarget(
            name: "A2UIFormDemo",
            dependencies: [
                .product(name: "AdaA2UI", package: "adaengine"),
                .product(name: "AdaEngine", package: "adaengine"),
                .product(name: "AdaPlatform", package: "adaengine")
            ],
            path: ".",
            exclude: ["README.md", "script"] + (FileManager.default.fileExists(atPath: "dist") ? ["dist"] : []),
            sources: [
                "A2UIFormDemo.swift"
            ],
            resources: [.copy("Fixtures")],
            swiftSettings: [.enableUpcomingFeature("MemberImportVisibility"), .strictMemorySafety()]
        )
    ]
)
