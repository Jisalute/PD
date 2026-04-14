"""送货历史导入：日期解析（-、/、Excel 序列日）。"""

from datetime import date, datetime

import pandas as pd
import pytest

from app.intelligent_prediction.services.history_service import HistoryService


@pytest.fixture
def svc() -> HistoryService:
    return HistoryService()


def test_parse_iso_hyphen(svc: HistoryService) -> None:
    d, err = svc._parse_date_cell("2026-01-05")
    assert err is None
    assert d == date(2026, 1, 5)


def test_parse_iso_slash(svc: HistoryService) -> None:
    d, err = svc._parse_date_cell("2026/1/5")
    assert err is None
    assert d == date(2026, 1, 5)


def test_parse_with_time(svc: HistoryService) -> None:
    d, err = svc._parse_date_cell("2026/03/15 00:00:00")
    assert err is None
    assert d == date(2026, 3, 15)


def test_parse_excel_serial(svc: HistoryService) -> None:
    d, err = svc._parse_date_cell(46027)
    assert err is None
    assert d == date(2026, 1, 5)


def test_parse_datetime_pandas(svc: HistoryService) -> None:
    d, err = svc._parse_date_cell(pd.Timestamp("2025-12-01"))
    assert err is None
    assert d == date(2025, 12, 1)


def test_parse_datetime_native(svc: HistoryService) -> None:
    d, err = svc._parse_date_cell(datetime(2024, 6, 30, 12, 0, 0))
    assert err is None
    assert d == date(2024, 6, 30)
