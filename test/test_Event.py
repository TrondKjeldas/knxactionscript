import unittest

from knxactionscript.event import Event


class TestEvent(unittest.TestCase):

    def setUp(self):

        pass

    def test_no_match(self):

        e = Event("X", 0)
        e.addAction("a1")
        e.addAction("a2")

        a = e.match(1)

        self.assertEqual(a, [])

    def test_match_val(self):

        e = Event("X", 0)
        e.addAction("a1")
        e.addAction("a2")

        a = e.match(0)

        self.assertEqual(a, ["a1", "a2"])

    def test_match_star(self):

        e = Event("X", "*")
        e.addAction("a1")
        e.addAction("a2")

        a = e.match(10)

        self.assertEqual(a, ["a1", "a2"])


if __name__ == '__main__':
    unittest.main()
