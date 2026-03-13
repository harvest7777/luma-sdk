from datetime import datetime, timezone

import pytest

from luma_sdk.utils.datetime import parse_dt


def test_returns_none_for_none():
    assert parse_dt(None) is None


def test_parses_utc_z_suffix():
    result = parse_dt("2024-06-15T18:30:00Z")
    assert result == datetime(2024, 6, 15, 18, 30, 0, tzinfo=timezone.utc)


def test_parses_explicit_utc_offset():
    result = parse_dt("2024-06-15T18:30:00+00:00")
    assert result == datetime(2024, 6, 15, 18, 30, 0, tzinfo=timezone.utc)


def test_result_is_timezone_aware():
    result = parse_dt("2024-01-01T00:00:00Z")
    assert result.tzinfo is not None


def test_parses_with_microseconds():
    result = parse_dt("2024-06-15T18:30:00.123456Z")
    assert result.microsecond == 123456
