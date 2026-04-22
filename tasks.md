import unittest
from lib.schema_config import FILES, NODES, FLOW, OC_PRIMS

class TestSchema(unittest.TestCase):
    def test_schema_loaded(self):
        self.assertGreater(len(FILES), 10)
        self.assertIn("USER", NODES)
        self.assertIn("VERIFIER", NODES)
        self.assertIn("PROMPT_SPLITTER", NODES)
        self.assertTrue(any("VERIFIER" in edge for edge in FLOW))

    def test_oc_primitives(self):
        self.assertIn("channels_inbound", OC_PRIMS)
        self.assertIn("runtimes", OC_PRIMS)

if __name__ == "__main__":
    unittest.main()
