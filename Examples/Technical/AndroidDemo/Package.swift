// swift-tools-version: 6.2
import Foundation
import PackageDescription

let package = Package(
    name: "AndroidDemo",
    platforms: [.macOS(.v15), .iOS(.v18)],
    products: [.library(name: "AndroidDemo", type: .dynamic, targets: ["AndroidDemo"])],
    dependencies: [
        .package(url: "https://github.com/AdaEngine/AdaEngine.git", revision: "b43d7e8f2f03e124a62b77499f7c2949a078dc27")
    ],
    targets: [
        .target(
            name: "AndroidDemo",
            dependencies: [
                .product(name: "AdaEngine", package: "adaengine"),
                .product(name: "CAndroid", package: "adaengine"),
                .product(name: "AdaPlatform", package: "adaengine")
            ],
            path: ".",
            exclude: ["README.md"] + (FileManager.default.fileExists(atPath: "dist") ? ["dist"] : []),
            sources: [
                "AndroidDemo.swift"
            ],
            resources: [.copy("Assets")],
            swiftSettings: [.enableUpcomingFeature("MemberImportVisibility"), .strictMemorySafety()]
        )
    ]
)
