"""schedapi.py：对外门面（老接口 spawn/run 不能改）。"""
from __future__ import annotations

from coroutine import Scheduler


class Runtime:
    def __init__(self, quantum: int = 2):
        self.scheduler = Scheduler(quantum)

    def spawn(self, task: str, steps) -> dict:
        return self.scheduler.spawn(task, steps)

    def wake(self, event: str) -> dict:
        return self.scheduler.wake(event)

    def run(self, max_ticks: int) -> dict:
        return self.scheduler.run(max_ticks)

    def snapshot(self) -> bytes:
        return self.scheduler.persist()

    def rebuild(self, blob: bytes = None) -> dict:
        return self.scheduler.restore(blob)
