import pytest

SENSITIVE_HEADER_KEYWORDS = {
    "authorization",
    "api-key",
    "token",
    "secret",
}

@pytest.fixture(scope="session")
def vcr_config():
    def scrub_sensitive_headers(request):
        for header in list(request.headers.keys()):
            if any(k in header.lower() for k in SENSITIVE_HEADER_KEYWORDS):
                request.headers[header] = "XXXXXXXXX REDACTED XXXXXXXXX"
        return request

    return {
        "record_mode": "once",
        "match_on": ["method", "scheme", "host", "port", "path", "query"],
        "before_record_request": scrub_sensitive_headers,
    }