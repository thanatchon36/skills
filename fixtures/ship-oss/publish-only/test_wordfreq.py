import unittest

from wordfreq import top_words


class TopWords(unittest.TestCase):
    def test_counts(self):
        self.assertEqual(top_words("a b a", 1), [("a", 2)])


if __name__ == "__main__":
    unittest.main()
