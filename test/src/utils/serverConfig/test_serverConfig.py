import unittest


class TestServerConfig(unittest.TestCase):

    def test_serverconfig(self):
        #ARRANGE
        expectedValue = 2

        #ACT
        actualValue = 2

        #ASSERT
        self.assertEqual(expectedValue, actualValue)