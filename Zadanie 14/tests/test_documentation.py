# tests/test_documentation.py

import unittest
import subprocess

class TestDocumentation(unittest.TestCase):
    def test_generate_documentation(self):
        # Run Sphinx to generate documentation
        result = subprocess.run(['sphinx-build', '-b', 'html', 'docs', 'docs/_build'])
        self.assertEqual(result.returncode, 0)

if __name__ == '__main__':
    unittest.main()
