// swift-tools-version: 6.2
import Foundation
import PackageDescription

let enginePath = ProcessInfo.processInfo.environment["ADAENGINE_PACKAGE_PATH"]
let engineDependency: Package.Dependency = enginePath.map { .package(name: "AdaEngine", path: $0) }
    ?? .package(url: "https://github.com/AdaEngine/AdaEngine.git", revision: "a624ccded0a050fddc24ccfbb8079dfb8032805c")

let mcpPath = ProcessInfo.processInfo.environment["ADA_MCP_LOCAL_PATH"]
let mcpDependency: Package.Dependency = mcpPath.map { .package(name: "AdaMCP", path: $0) }
    ?? .package(url: "https://github.com/AdaEngine/AdaMCP.git", exact: "0.2.0")

let package = Package(
    name: "SpineNative",
    platforms: [.macOS(.v15), .iOS(.v18)],
    products: [.executable(name: "SpineNative", targets: ["SpineNative"])],
    dependencies: [
        engineDependency,
        mcpDependency
    ],
    targets: [
        .executableTarget(
            name: "SpineNative",
            dependencies: [
                .product(name: "AdaEngine", package: "adaengine"),
                .product(name: "AdaSpine", package: "adaengine"),
                .product(name: "AdaMCPPlugin", package: "AdaMCP")
            ],
            path: ".",
            exclude: ["README.md", "capture.py"] + (FileManager.default.fileExists(atPath: "dist") ? ["dist"] : []),
            sources: [
                "SpineNativeApp.swift"
            ],
            swiftSettings: [.enableUpcomingFeature("MemberImportVisibility"), .strictMemorySafety()]
        )
    ]
)
