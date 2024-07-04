# tests/test_coverage.py

import unittest
import pytest

class TestCoverage(unittest.TestCase):
    def test_coverage(self):
        # Run pytest with coverage and check if it meets the threshold
        result = pytest.main(['--cov=app', '--cov-report=term-missing'])
        coverage_percentage = result.get_result().coverage
        self.assertGreaterEqual(coverage_percentage, 95)

if __name__ == '__main__':
    unittest.main()
