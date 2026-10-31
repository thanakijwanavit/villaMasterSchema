import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ("group/tester.ipynb", "userinfo/tester.ipynb")
STALE_REFERENCES = (
    "TestValidation",
    "order.yaml",
    "goodSample.json",
    "wrongType.json",
    "extraCol.json",
    "add_method",
)


class NotebookValidationCells(unittest.TestCase):
    def test_only_directory_specific_schema_validation_remains(self):
        for relative_path in NOTEBOOKS:
            with self.subTest(notebook=relative_path):
                notebook = json.loads((ROOT / relative_path).read_text(encoding="utf-8"))
                code = "\n".join(
                    "".join(cell.get("source", []))
                    if isinstance(cell.get("source", []), list)
                    else cell.get("source", "")
                    for cell in notebook["cells"]
                    if cell["cell_type"] == "code"
                )
                self.assertIn("def test_schema()", code)
                for reference in STALE_REFERENCES:
                    self.assertNotIn(reference, code)


if __name__ == "__main__":
    unittest.main()
