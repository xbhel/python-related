import unittest
import sideeffects  # noqa: F401
import utils


class UtilsTestCase(unittest.TestCase):
    def test_isafter(self):
        epochseconds = utils.TimeUtil.str2epochseconds(
            "2024-07-19", "%Y-%m-%d", utils.TimeUtil.ASIA_SHANGHAI
        )
        result = utils.is_after(epochseconds, "2024-07-20")
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
