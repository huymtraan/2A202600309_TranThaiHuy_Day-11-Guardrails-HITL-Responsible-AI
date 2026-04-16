"""Rate limiting (sliding window, per-user)."""

from __future__ import annotations

import time
from collections import defaultdict, deque
from dataclasses import dataclass


@dataclass(frozen=True)
class RateLimitDecision:
    allowed: bool
    wait_seconds: float = 0.0
    reason: str = ""


class RateLimiter:
    """Sliding-window rate limiter.

    Why:
        A dedicated abuse-control layer stops request floods before they reach
        costly model calls or deeper safety checks.
    """

    def __init__(self, *, max_requests: int = 10, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._windows: dict[str, deque[float]] = defaultdict(deque)

    def check(self, *, user_id: str, now: float | None = None) -> RateLimitDecision:
        """Evaluate whether this request is allowed in the active window.

        Why:
            Returning `wait_seconds` lets the caller show transparent retry
            guidance in logs and notebook outputs.
        """
        now_ts = time.time() if now is None else now
        window = self._windows[user_id]

        cutoff = now_ts - self.window_seconds
        while window and window[0] < cutoff:
            window.popleft()

        if len(window) >= self.max_requests:
            wait = max(0.0, (window[0] + self.window_seconds) - now_ts)
            return RateLimitDecision(
                allowed=False,
                wait_seconds=wait,
                reason=f"Rate limit exceeded: max {self.max_requests}/{self.window_seconds}s",
            )

        window.append(now_ts)
        return RateLimitDecision(allowed=True)
