// swift-tools-version: 6.2
import Foundation
import PackageDescription

let package = Package(
    name: "LinuxSmoke",
    platforms: [.macOS(.v15), .iOS(.v18)],
    products: [.executable(name: "LinuxSmoke", targets: ["LinuxSmoke"])],
    dependencies: [
        .package(url: "https://github.com/AdaEngine/AdaEngine.git", revision: "b43d7e8f2f03e124a62b77499f7c2949a078dc27")
    ],
    targets: [
        .executableTarget(
            name: "LinuxSmoke",
            dependencies: [
                .product(name: "AdaEngine", package: "adaengine"),
                .product(name: "AdaPlatform", package: "adaengine")
            ],
            path: ".",
            exclude: ["README.md"] + (FileManager.default.fileExists(atPath: "dist") ? ["dist"] : []),
            sources: [
                "LinuxSmoke.swift"
            ],
            swiftSettings: [.enableUpcomingFeature("MemberImportVisibility"), .strictMemorySafety()]
        )
    ]
)
