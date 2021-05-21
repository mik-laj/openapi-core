import pytest

from six import b


class TestDjangoRESTFrameworkAPIView(object):

    @pytest.fixture
    def http_client(self):
        from django.test import Client
        return Client()

    def test_get(self, http_client):
        response = http_client.get('/api/test-simple/')

        assert response.content == b('{"test": "test_val"}')
