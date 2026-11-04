// swift-tools-version: 6.2
import Foundation
import PackageDescription

let package = Package(
    name: "SpriteInstancingValidation",
    platforms: [.macOS(.v15), .iOS(.v18)],
    products: [.executable(name: "SpriteInstancingValidation", targets: ["SpriteInstancingValidation"])],
    dependencies: [
        .package(url: "https://github.com/AdaEngine/AdaEngine.git", revision: "a624ccded0a050fddc24ccfbb8079dfb8032805c")
    ],
    targets: [
        .executableTarget(
            name: "SpriteInstancingValidation",
            dependencies: [
                .product(name: "AdaApp", package: "adaengine"),
                .product(name: "AdaAssets", package: "adaengine"),
                .product(name: "AdaCorePipelines", package: "adaengine"),
                .product(name: "AdaECS", package: "adaengine"),
                .product(name: "AdaInput", package: "adaengine"),
                .product(name: "AdaPlatform", package: "adaengine"),
                .product(name: "AdaRender", package: "adaengine"),
                .product(name: "AdaSprite", package: "adaengine"),
                .product(name: "AdaText", package: "adaengine"),
                .product(name: "AdaTransform", package: "adaengine"),
                .product(name: "AdaUI", package: "adaengine"),
                .product(name: "AdaUtils", package: "adaengine"),
                .product(name: "Math", package: "adaengine")
            ],
            path: ".",
            exclude: ["README.md", "project.yml"] + (FileManager.default.fileExists(atPath: "dist") ? ["dist"] : []),
            sources: [
                "SpriteValidationApp.swift",
                "SpriteValidationFixture.swift"
            ],
            swiftSettings: [.enableUpcomingFeature("MemberImportVisibility"), .strictMemorySafety()],
            linkerSettings: [.unsafeFlags([
                "-Xclang-linker", "-mexec-model=reactor",
                "-Xlinker", "--export-if-defined=main",
                "-Xlinker", "--export-if-defined=__main_argc_argv"
            ], .when(platforms: [.wasi]))]
        )
    ]
)
