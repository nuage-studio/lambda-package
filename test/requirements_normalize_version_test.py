import unittest

from lambda_package.requirements import normalize_version


class RequirementsNormalizeVersionTests(unittest.TestCase):
    """
    Unit tests for the `requirements.normalize_version` function
    """

    def test_when_call_with_valid_version_then_no_change(self):
        result = normalize_version("5.2")
        self.assertEqual("5.2", result)

    def test_when_call_with_patch_then_remove_patch(self):
        result = normalize_version("5.2.6")
        self.assertEqual("5.2", result)

    def test_when_call_with_major_only_then_error(self):
        self.assertRaises(ValueError, normalize_version, "5")

    def test_when_call_with_invalid_then_error(self):
        self.assertRaises(ValueError, normalize_version, "a.b")
