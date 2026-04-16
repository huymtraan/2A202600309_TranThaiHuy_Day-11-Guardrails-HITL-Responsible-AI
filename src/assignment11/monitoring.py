"""Monitoring and alerting (simple counters + thresholds)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Metrics:
    total: int = 0
    blocked: int = 0
    rate_limited: int = 0
    judge_failed: int = 0
    redacted: int = 0

    def block_rate(self) -> float:
        """Current fraction of blocked requests.

        Why:
            Sudden block-rate spikes usually indicate active probing/attacks.
        """
        return (self.blocked / self.total) if self.total else 0.0

    def judge_fail_rate(self) -> float:
        """Current fraction of requests failed by judge.

        Why:
            A high value suggests generation quality or policy drift.
        """
        return (self.judge_failed / self.total) if self.total else 0.0


class Monitor:
    """Tracks metrics and emits alerts.

    Why:
        Monitoring closes the loop from prevention to operations by surfacing
        anomaly signals during tests and production-like runs.
    """

    def __init__(
        self,
        *,
        alert_block_rate: float = 0.6,
        alert_judge_fail_rate: float = 0.3,
        alert_rate_limit_hits: int = 5,
    ):
        self.metrics = Metrics()
        self.alert_block_rate = alert_block_rate
        self.alert_judge_fail_rate = alert_judge_fail_rate
        self.alert_rate_limit_hits = alert_rate_limit_hits

    def record(
        self,
        *,
        blocked: bool,
        rate_limited: bool,
        judge_failed: bool,
        redacted: bool,
    ) -> list[str]:
        """Update counters for one request and return active alerts.

        Why:
            Real-time checks make it obvious when safety posture degrades.
        """
        m = self.metrics
        m.total += 1
        if blocked:
            m.blocked += 1
        if rate_limited:
            m.rate_limited += 1
        if judge_failed:
            m.judge_failed += 1
        if redacted:
            m.redacted += 1
        return self.check_alerts()

    def check_alerts(self) -> list[str]:
        """Evaluate alert thresholds from current aggregate metrics."""
        alerts: list[str] = []
        if self.metrics.total >= 10 and self.metrics.block_rate() >= self.alert_block_rate:
            alerts.append(f"ALERT: high block rate {self.metrics.block_rate():.0%}")
        if self.metrics.total >= 10 and self.metrics.judge_fail_rate() >= self.alert_judge_fail_rate:
            alerts.append(f"ALERT: high judge-fail rate {self.metrics.judge_fail_rate():.0%}")
        if self.metrics.rate_limited >= self.alert_rate_limit_hits:
            alerts.append(f"ALERT: frequent rate limiting ({self.metrics.rate_limited})")
        return alerts
