// swift-tools-version: 6.2
import Foundation
import PackageDescription

let package = Package(
    name: "Physics2DDemo",
    platforms: [.macOS(.v15), .iOS(.v18)],
    products: [.executable(name: "Physics2DDemo", targets: ["Physics2DDemo"])],
    dependencies: [
        .package(url: "https://github.com/AdaEngine/AdaEngine.git", revision: "b43d7e8f2f03e124a62b77499f7c2949a078dc27")
    ],
    targets: [
        .executableTarget(
            name: "Physics2DDemo",
            dependencies: [
                .product(name: "AdaEngine", package: "adaengine"),
                .product(name: "AdaApp", package: "adaengine"),
                .product(name: "AdaPlatform", package: "adaengine"),
                .product(name: "Math", package: "adaengine")
            ],
            path: ".",
            exclude: ["README.md", "script"] + (FileManager.default.fileExists(atPath: "dist") ? ["dist"] : []),
            sources: [
                "Physics2DAdvancedChecks.swift",
                "Physics2DAdvancedDemo.swift",
                "Physics2DCharactersDemo.swift",
                "Physics2DDemoMain.swift",
                "Physics2DDemoScenes.swift",
                "Physics2DDemoView.swift",
                "Physics2DLargeWorldChecks.swift",
                "Physics2DLargeWorldDemo.swift",
                "Physics2DMechanismsDemo.swift",
                "Physics2DQueriesDemo.swift"
            ],
            swiftSettings: [.enableUpcomingFeature("MemberImportVisibility"), .strictMemorySafety()]
        )
    ]
)
