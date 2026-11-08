from __future__ import annotations


def test_invalid_scheme_javascript(client):
    response = client.post(
        "/api/links",
        json={"url": "javascript:alert(1)"},
    )
    assert response.status_code == 400


def test_invalid_scheme_data(client):
    response = client.post(
        "/api/links",
        json={"url": "data:text/html,hi"},
    )
    assert response.status_code == 400


def test_invalid_scheme_ftp(client):
    response = client.post(
        "/api/links",
        json={"url": "ftp://files.example.com/a"},
    )
    assert response.status_code == 400


def test_invalid_scheme_file(client):
    response = client.post(
        "/api/links",
        json={"url": "file:///etc/passwd"},
    )
    assert response.status_code == 400


def test_url_missing_netloc(client):
    response = client.post(
        "/api/links",
        json={"url": "https:///path-only"},
    )
    assert response.status_code == 400


def test_url_too_long(client):
    long_url = "https://example.com/" + ("a" * 2100)
    response = client.post(
        "/api/links",
        json={"url": long_url},
    )
    assert response.status_code == 400
