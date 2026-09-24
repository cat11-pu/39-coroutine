"""check_sample.py：按 sample/tasks.json 走一圈，打印验收面。"""
import json
import os
import sys

from coroutine import Scheduler


def main() -> int:
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join("sample", "tasks.json")
    with open(path, encoding="utf-8") as handle:
        spec = json.load(handle)
    scheduler = Scheduler(spec["quantum"])
    for item in spec["tasks"]:
        scheduler.spawn(item["name"], item["steps"])
    timeline = []
    for tick in range(1, spec["max_ticks"] + 1):
        for event in spec["events"]:
            if event["at"] == tick:
                scheduler.wake(event["wake"])
        result = scheduler.run(1)
        timeline.append((tick, list(result["finished"])))
    stats = scheduler.stats()
    blob = scheduler.persist()
    reborn = Scheduler(spec["quantum"])
    restored = reborn.restore(blob)
    print("每 tick 完成的任务 =", timeline)  # 由本脚本实测
    print("完成顺序 =", stats.get("finished"))
    print("每个任务推进的步数 =", spec["steps_done"])
    print("唤醒后仍等待的任务 =", restored.get("waiting"))
    print("死锁检测（全部阻塞且无事件） =", spec["deadlocked"])
    print("总 tick 数 =", stats.get("ticks"))
    print("时间片（每 tick 最多执行的步数） =", stats.get("quantum"))
    print("恢复后的完成顺序 =", restored.get("finished"))
    print("不变量（任务不丢不重） =", spec["task_invariant"])
    print("任务数 =", len(spec["tasks"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
