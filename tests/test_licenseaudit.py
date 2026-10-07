import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from licenseaudit import core


class LicenseAuditTest(unittest.TestCase):
    def test_allowed_license(self):
        out = core.audit({"root": []}, ["root"], {"root": "MIT"},
                         {"MIT"}, set(), set(), core.Counter())
        self.assertEqual(out, [])

    def test_missing_license_is_violation(self):
        out = core.audit({"root": []}, ["root"], {},
                         {"MIT"}, set(), set(), core.Counter())
        self.assertEqual(out, ["root"])

    def test_empty_roots(self):
        self.assertEqual(core.audit({}, [], {}, set(), set(), set(), core.Counter()), [])

    def test_returns_list(self):
        out = core.audit({"root": []}, ["root"], {"root": "MIT"},
                         {"MIT"}, set(), set(), core.Counter())
        self.assertIsInstance(out, list)

    def test_direct_dep_reachable(self):
        out = core.audit({"root": ["a"], "a": []}, ["root"], {"root": "MIT", "a": "MIT"},
                         {"MIT"}, set(), set(), core.Counter())
        self.assertEqual(out, [])

    def test_counter_counts(self):
        counter = core.Counter()
        core.audit({"root": []}, ["root"], {"root": "MIT"}, {"MIT"}, set(), set(), counter)
        self.assertGreater(counter.scanned, 0)


if __name__ == "__main__":
    unittest.main()
