// swift-tools-version: 6.2
import Foundation
import PackageDescription

let package = Package(
    name: "SpinePreview",
    platforms: [.macOS(.v15), .iOS(.v18)],
    products: [.executable(name: "SpinePreview", targets: ["SpinePreview"])],
    dependencies: [
        .package(url: "https://github.com/AdaEngine/AdaEngine.git", revision: "b43d7e8f2f03e124a62b77499f7c2949a078dc27")
    ],
    targets: [
        .executableTarget(
            name: "SpinePreview",
            dependencies: [
                .product(name: "AdaSpineRuntime", package: "adaengine")
            ],
            path: ".",
            exclude: ["README.md"] + (FileManager.default.fileExists(atPath: "dist") ? ["dist"] : []),
            sources: [
                "SpinePreview.swift"
            ],
            resources: [.copy("Assets")],
            swiftSettings: [.enableUpcomingFeature("MemberImportVisibility"), .strictMemorySafety()]
        )
    ]
)
