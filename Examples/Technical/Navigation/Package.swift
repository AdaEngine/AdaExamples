// swift-tools-version: 6.2
import Foundation
import PackageDescription

let package = Package(
    name: "NavigationDemo",
    platforms: [.macOS(.v15), .iOS(.v18)],
    products: [.executable(name: "NavigationDemo", targets: ["NavigationDemo"])],
    dependencies: [
        .package(url: "https://github.com/AdaEngine/AdaEngine.git", revision: "a624ccded0a050fddc24ccfbb8079dfb8032805c")
    ],
    targets: [
        .executableTarget(
            name: "NavigationDemo",
            dependencies: [
                .product(name: "AdaEngine", package: "adaengine"),
                .product(name: "AdaNavigationBaking", package: "adaengine"),
                .product(name: "AdaApp", package: "adaengine")
            ],
            path: ".",
            exclude: ["README.md", "script"] + (FileManager.default.fileExists(atPath: "dist") ? ["dist"] : []),
            sources: [
                "NavigationDemoApp.swift",
                "NavigationDemoFixture.swift",
                "NavigationDemoMain.swift",
                "NavigationDemoScript.swift"
            ],
            resources: [.copy("NavigationRobot.ada")],
            swiftSettings: [.enableUpcomingFeature("MemberImportVisibility"), .strictMemorySafety()]
        )
    ]
)
