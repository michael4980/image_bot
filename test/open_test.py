import httpx
import pytest


def test_default(respx_mock):
    respx_mock.get("https://foo.bar/").mock(return_value=httpx.Response(204))
    response = httpx.get("https://foo.bar/")
    assert response.status_code == 204


@pytest.mark.respx(base_url="https://foo.bar")
def test_with_marker(respx_mock):
    respx_mock.get("/baz/").mock(return_value=httpx.Response(204))
    response = httpx.get("https://foo.bar/baz/")
    assert response.status_code == 204



