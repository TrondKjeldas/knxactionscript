import unittest

from knxactionscript.knxevent import KnxEvent


class TestEvent(unittest.TestCase):

    def setUp(self):

        pass

    def test_no_match(self):

        e = KnxEvent("X", "1/2/3", 0)
        e.addAction("a1")
        e.addAction("a2")

        a = e.match("1/2/4", 0)
        self.assertEqual(a, [])

        a = e.match("1/2/3", 1)
        self.assertEqual(a, [])

        a = e.match("1/2/4", 1)
        self.assertEqual(a, [])

    def test_match_grp_and_val(self):

        e = KnxEvent("X", "1/2/3", 0)
        e.addAction("a1")
        e.addAction("a2")

        a = e.match("1/2/3", 0)

        self.assertEqual(a, ["a1", "a2"])

    def test_match_grp_and_star(self):

        e = KnxEvent("X", "1/2/3", "*")
        e.addAction("a1")
        e.addAction("a2")

        a = e.match("1/2/3", 10)

        self.assertEqual(a, ["a1", "a2"])


if __name__ == '__main__':
    unittest.main()
