from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from src.pages.map_embed import normalize_google_maps_embed

EMBED_URL = (
    'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d5080.73235292209'
    '!2d30.51162857654071!3d50.45290558718699!2m3!1f0!2f0!3f0!3m2!1i1024'
    '!2i768!4f13.1!3m3!1m2!1s0x40d4ce88e35e395f%3A0xc63774cf5da5a434'
    '!2z0KHQvtGE0ZbQudGB0YzQutC40Lkg0YHQvtCx0L7RgA!5e0!3m2!1suk!2sua'
    '!4v1785828669394!5m2!1suk!2sua'
)

IFRAME = (
    f'<iframe src="{EMBED_URL}" width="600" height="450" style="border:0;" '
    'allowfullscreen="" loading="lazy" '
    'referrerpolicy="strict-origin-when-cross-origin"></iframe>'
)


class NormalizeGoogleMapsEmbedTests(SimpleTestCase):
    def test_empty_allowed(self):
        self.assertEqual(normalize_google_maps_embed(''), '')
        self.assertEqual(normalize_google_maps_embed('   '), '')

    def test_extracts_src_from_iframe(self):
        self.assertEqual(normalize_google_maps_embed(IFRAME), EMBED_URL)

    def test_accepts_plain_embed_url(self):
        self.assertEqual(normalize_google_maps_embed(EMBED_URL), EMBED_URL)

    def test_rejects_non_google(self):
        with self.assertRaises(ValidationError):
            normalize_google_maps_embed('https://example.com/maps/embed?q=1')

    def test_rejects_iframe_without_src(self):
        with self.assertRaises(ValidationError):
            normalize_google_maps_embed('<iframe width="600"></iframe>')
