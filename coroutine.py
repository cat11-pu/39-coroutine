"""coroutine.py：协作式调度（基线：逐个跑完，无时间片、无唤醒）。"""
from __future__ import annotations


class Scheduler:
    def __init__(self, quantum: int = 2):
        self.quantum = quantum
        self.tasks = {}
        self.ready = []
        self.waiting = {}
        self.finished = []
        self.ticks = 0

    def spawn(self, task: str, steps) -> dict:
        self.tasks[task] = {"steps": list(steps), "index": 0}
        self.ready.append(task)
        return {"tasks": len(self.tasks)}

    def wake(self, event: str) -> dict:
        raise NotImplementedError("事件唤醒还没实现")

    def run(self, max_ticks: int) -> dict:
        """基线：就绪队列里的任务一次性跑到底，不看 quantum。"""
        while self.ready and self.ticks < max_ticks:
            task = self.ready.pop(0)
            state = self.tasks[task]
            while state["index"] < len(state["steps"]):
                state["index"] += 1
            self.ticks += 1
            self.finished.append(task)
        return {"ticks": self.ticks, "finished": list(self.finished)}

    def recover(self) -> dict:
        raise NotImplementedError("重启恢复还没实现")

    def stats(self) -> dict:
        return {"ticks": self.ticks, "ready": list(self.ready), "waiting": {k: list(v) for k, v in self.waiting.items()},
                "finished": list(self.finished), "quantum": self.quantum}
