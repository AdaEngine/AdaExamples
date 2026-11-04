"""Validate standalone technical SwiftPM manifests without downloading dependencies or building apps."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]


def manifest(path, swift):
    result = subprocess.run([swift, "package", "--package-path", str(path), "dump-package"],
                            capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine-root", type=Path, help="Also check products against a local engine manifest")
    args = parser.parse_args()
    swift = shutil.which("swift")
    if not swift:
        parser.error("Swift 6.2 or later is required")
    products = None
    if args.engine_root:
        engine = manifest(args.engine_root.resolve(), swift)
        products = {item["name"] for item in engine["products"]}
        assert all(not (item.get("path") or "").startswith("Demos/") for item in engine["targets"])
    public = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    public_paths = {item["path"] for item in public["items"]}
    paths = sorted((ROOT / "Examples/Technical").glob("*/Package.swift"))
    for path in paths:
        data = manifest(path.parent, swift)
        assert path.parent.relative_to(ROOT).as_posix() not in public_paths
        for dependency in data["dependencies"]:
            assert "fileSystem" not in dependency, "Unset local dependency overrides when validating distribution manifests"
            for source in dependency.get("sourceControl", []):
                assert source["requirement"].get("revision") or source["requirement"].get("exact"), "Pin technical dependencies"
        for target in data["targets"]:
            folder = path.parent / target.get("path", ".")
            assert folder.is_dir(), folder
            for source in target.get("sources") or []:
                assert source != "Package.swift", "Do not compile the package manifest as application code"
                assert (folder / source).is_file(), source
            for resource in target.get("resources", []):
                assert (folder / resource["path"]).exists(), resource
            if products:
                for dependency in target["dependencies"]:
                    product = dependency.get("product")
                    if product and product[1].lower() == "adaengine":
                        assert product[0] in products, f"Missing engine product {product[0]}"
        print(f"manifest ok: {path.parent.name}", flush=True)
    print(f"Validated {len(paths)} technical packages; native builds and device execution are separate checks.")


if __name__ == "__main__":
    main()
