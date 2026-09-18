import unittest

from add_clip import add_clip, normalize_name, slugify, youtube_id


class AddClipTest(unittest.TestCase):
    def test_normalizes_animal_names(self):
        self.assertEqual(normalize_name("  Red   FOX  "), "red fox")
        self.assertEqual(slugify("Rød Panda"), "rd-panda")

    def test_reads_supported_youtube_urls(self):
        self.assertEqual(youtube_id("https://www.youtube.com/shorts/0dbu5Q3l-yM"), "0dbu5Q3l-yM")
        self.assertEqual(youtube_id("https://youtu.be/0dbu5Q3l-yM"), "0dbu5Q3l-yM")

    def test_creates_animal_and_appends_to_existing_animal(self):
        catalog = {"animals": []}
        add_clip(catalog, " Sea Lion ", "https://youtu.be/0dbu5Q3l-yM")
        add_clip(catalog, "sea lion", "https://youtu.be/oN7axlCqiG4")

        self.assertEqual(len(catalog["animals"]), 1)
        self.assertEqual(catalog["animals"][0]["name"], "sea lion")
        self.assertEqual(catalog["animals"][0]["id"], "sea-lion")
        self.assertEqual(len(catalog["animals"][0]["sources"]), 2)

    def test_rejects_duplicate_video(self):
        catalog = {"animals": []}
        add_clip(catalog, "lion", "https://youtu.be/0dbu5Q3l-yM")
        with self.assertRaisesRegex(ValueError, "already in the catalog"):
            add_clip(catalog, "seal", "https://youtu.be/0dbu5Q3l-yM")


if __name__ == "__main__":
    unittest.main()
