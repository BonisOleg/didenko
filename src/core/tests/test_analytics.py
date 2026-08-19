from django.template import Context
from django.template.loader import get_template
from django.test import RequestFactory, SimpleTestCase

from src.core.context_processors import _clean_tag_id


class CleanTagIdTests(SimpleTestCase):
    def test_accepts_gtm_and_ads_ids(self):
        self.assertEqual(_clean_tag_id('GTM-WVJDC8DM'), 'GTM-WVJDC8DM')
        self.assertEqual(_clean_tag_id('AW-18394859385'), 'AW-18394859385')

    def test_rejects_injection(self):
        self.assertEqual(_clean_tag_id("GTM-1';alert(1)//"), '')
        self.assertEqual(_clean_tag_id(''), '')


class AnalyticsPartialsTests(SimpleTestCase):
    def setUp(self):
        request = RequestFactory().get('/')
        request.csp_nonce = 'test-nonce'
        self.request = request

    def _render(self, template_name, context):
        context['request'] = self.request
        return get_template(template_name).template.render(Context(context))

    def test_head_renders_gtm_and_google_tag(self):
        html = self._render(
            'partials/analytics_head.html',
            {
                'gtm_container_id': 'GTM-WVJDC8DM',
                'google_tag_id': 'AW-18394859385',
            },
        )
        self.assertIn('GTM-WVJDC8DM', html)
        self.assertIn('AW-18394859385', html)
        self.assertIn('nonce="test-nonce"', html)
        self.assertIn('gtag/js?id=AW-18394859385', html)

    def test_body_renders_gtm_noscript(self):
        html = self._render(
            'partials/analytics_body.html',
            {'gtm_container_id': 'GTM-WVJDC8DM'},
        )
        self.assertIn('ns.html?id=GTM-WVJDC8DM', html)

    def test_empty_ids_render_nothing(self):
        head = self._render(
            'partials/analytics_head.html',
            {'gtm_container_id': '', 'google_tag_id': ''},
        )
        body = self._render(
            'partials/analytics_body.html',
            {'gtm_container_id': ''},
        )
        self.assertNotIn('googletagmanager.com', head)
        self.assertNotIn('googletagmanager.com', body)
