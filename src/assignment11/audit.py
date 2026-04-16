"""Audit logging utilities."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


@dataclass
class AuditEvent:
    ts: float
    user_id: str
    input_text: str
    allowed: bool
    blocked_by: str | None
    reason: str | None
    model: str | None
    output_text: str | None
    output_original: str | None
    output_redacted: str | None
    judge: dict[str, Any] | None
    latency_ms: int


class AuditLogger:
    """In-memory audit log with JSON export.

    Why:
        Audit trails are required to explain which layer blocked/modified
        content and to support post-incident analysis.
    """

    def __init__(self):
        self.events: list[AuditEvent] = []

    def log(self, event: AuditEvent) -> None:
        """Append one event to the audit stream."""
        self.events.append(event)

    def export_json(self, path: str | Path) -> None:
        """Write all events to disk as UTF-8 JSON.

        Why:
            The assignment requires exported evidence for test outcomes.
        """
        out = [asdict(e) for e in self.events]
        Path(path).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    @staticmethod
    def now() -> float:
        return time.time()
