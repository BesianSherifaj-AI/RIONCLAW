import tempfile, unittest
from pathlib import Path
from lib.md_io import append, patch, replace, read

class TestMdIo(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        self.dir = Path(self.td.name)
    def tearDown(self):
        self.td.cleanup()

    def test_append_creates_entry(self):
        p = self.dir / "x.md"
        append(p, "first entry", writer="test", reason="t")
        append(p, "second entry", writer="test", reason="t")
        body = p.read_text()
        self.assertIn("first entry", body)
        self.assertIn("second entry", body)
        self.assertEqual(body.count("<!-- entry:"), 2)

    def test_patch_named_section(self):
        p = self.dir / "y.md"
        p.write_text("top\n<!-- begin:s -->\nold\n<!-- end:s -->\nbottom\n")
        res = patch(p, "s", "new", writer="test", reason="t")
        self.assertEqual(res, "patched")
        txt = p.read_text()
        self.assertIn("new", txt)
        self.assertNotIn("old", txt)
        self.assertIn("top", txt)
        self.assertIn("bottom", txt)

    def test_patch_missing_anchor_appends(self):
        p = self.dir / "z.md"
        p.write_text("some content\n")
        res = patch(p, "newsec", "body", writer="test", reason="t")
        self.assertEqual(res, "appended")
        txt = p.read_text()
        self.assertIn("<!-- begin:newsec -->", txt)
        self.assertIn("body", txt)

    def test_replace_archives_previous(self):
        p = self.dir / "ongoing.md"
        a = self.dir / "archived.md"
        p.write_text("old ongoing\n")
        replace(p, "new ongoing", writer="test", reason="rotate", archive_path=a)
        self.assertEqual(p.read_text().strip(), "new ongoing")
        self.assertIn("old ongoing", a.read_text())

if __name__ == "__main__":
    unittest.main()
