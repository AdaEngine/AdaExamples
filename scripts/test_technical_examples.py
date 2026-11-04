import contextlib
import io
import unittest

from validate_catalog import load_catalog, validate_catalog


class TechnicalExamplesTests(unittest.TestCase):
    def test_existing_catalog_still_validates(self):
        validate_catalog(load_catalog())

    def test_technical_project_cannot_enter_public_catalog(self):
        for path in ["Examples/Technical/ProceduralSkeleton", "Examples/./Technical/ProceduralSkeleton",
                     "Examples/Other/../Technical/ProceduralSkeleton"]:
            with self.subTest(path=path):
                catalog = load_catalog()
                catalog["items"].append({
                    **catalog["items"][0],
                    "id": "procedural-skeleton",
                    "kind": "example",
                    "path": path,
                })
                errors = io.StringIO()
                with contextlib.redirect_stderr(errors), self.assertRaises(SystemExit) as raised:
                    validate_catalog(catalog)
                self.assertEqual(raised.exception.code, 1)
                self.assertIn("technical examples must remain outside the public catalog", errors.getvalue())


if __name__ == "__main__":
    unittest.main()
