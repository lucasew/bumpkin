import pytest
from bumpkin.sources.basichttp import BasicHTTPSource
from bumpkin.sources.basichttpjsonvendor import BasicHTTPJSONVendorSource


def test_basic_http_source_ssrf_protection():
    with pytest.raises(ValueError, match="Invalid URL scheme"):
        BasicHTTPSource(url="file:///etc/passwd")


def test_basic_http_json_vendor_source_ssrf_protection():
    with pytest.raises(ValueError, match="Invalid URL scheme"):
        BasicHTTPJSONVendorSource(url="file:///etc/passwd")


def test_basic_http_source_ftp_protection():
    with pytest.raises(ValueError, match="Invalid URL scheme"):
        BasicHTTPSource(url="ftp://example.com/file")


def test_basic_http_source_valid_schemes():
    # Should not raise
    BasicHTTPSource(url="http://example.com/file")
    BasicHTTPSource(url="https://example.com/file")
