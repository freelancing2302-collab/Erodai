import asyncio
import sys
from datetime import datetime, time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.report_scheduler import ReportScheduler


@pytest.mark.asyncio
async def test_scheduler_targets_900_am(monkeypatch):
    scheduler = ReportScheduler()
    calls = []

    async def fake_send_alerts():
        calls.append("sent")

    monkeypatch.setattr(scheduler, "_send_alerts", fake_send_alerts)

    async def fake_sleep(_seconds):
        raise asyncio.CancelledError

    monkeypatch.setattr("app.services.report_scheduler.asyncio.sleep", fake_sleep)

    class FrozenDateTime(datetime):
        @classmethod
        def now(cls):
            return cls(2026, 7, 30, 9, 0, 0)

    monkeypatch.setattr("app.services.report_scheduler.datetime", FrozenDateTime)

    with pytest.raises(asyncio.CancelledError):
        await scheduler._run_scheduler()

    assert calls == ["sent"]


def test_scheduler_target_time_constant():
    assert ReportScheduler()._target_time() == time(9, 0, 0)
