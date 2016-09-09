from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from mock import patch
from django.test import override_settings
import httpretty
import json
from django.conf import settings

class HashCachTests(APITestCase):
    @override_settings(HASH_URL='http://example.com')
    def test_from_cache(self):
        httpretty.enable()
        with patch('hash_cache.views.cache') as mock_cache:
            cache = {}
            ttl = {}

            def get(key, default=None):
                return cache.get(key, default)

            def _set(key, value, timeout=60):
                cache[key] = value
                ttl[key] = timeout

            mock_cache.get = get
            mock_cache.set = _set


            json_body = json.dumps({'hash': '321'})
            httpretty.register_uri(httpretty.GET, 'http://example.com',
                                   body=json_body,
                                   content_type='application/json',
                                   status=200)

            url = "%s?key=""" % reverse('from_cache')
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual({}, cache)
            self.assertEqual(response.content, '""')


            url = "%s?key=123" % reverse('from_cache')
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.content, '"321"')
            self.assertEqual(cache.get('123'), '321')
            self.assertEqual(ttl.get('123'), settings.HASH_TTL)

            json_body = json.dumps({'hash': '456'})
            httpretty.register_uri(httpretty.GET, 'http://example.com',
                                   body=json_body,
                                   content_type='application/json',
                                   status=200)
            url = "%s?key=123" % reverse('from_cache')
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.content, '"321"')


            json_body = json.dumps("error")
            httpretty.register_uri(httpretty.GET, 'http://example.com',
                                   body=json_body,
                                   content_type='application/json',
                                   status=200)
            url = "%s?key=1234" % reverse('from_cache')
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.content, '""')

        httpretty.disable()
