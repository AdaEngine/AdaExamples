// swift-tools-version: 6.2
import Foundation
import PackageDescription

let package = Package(
    name: "A2UIFormDemo",
    platforms: [.macOS(.v15), .iOS(.v18)],
    products: [.executable(name: "A2UIFormDemo", targets: ["A2UIFormDemo"])],
    dependencies: [
        .package(url: "https://github.com/AdaEngine/AdaEngine.git", revision: "a624ccded0a050fddc24ccfbb8079dfb8032805c")
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
