import unittest

from coroutine import Scheduler
from schedapi import Runtime


class TestScheduler(unittest.TestCase):
    def test_spawn_counts(self):
        scheduler = Scheduler()
        self.assertEqual(scheduler.spawn("t1", ["cpu"])["tasks"], 1)

    def test_run_finishes_task(self):
        scheduler = Scheduler()
        scheduler.spawn("t1", ["cpu"])
        self.assertEqual(scheduler.run(4)["finished"], ["t1"])

    def test_stats_shape(self):
        self.assertIn("quantum", Scheduler().stats())

    def test_ready_after_spawn(self):
        scheduler = Scheduler()
        scheduler.spawn("t1", ["cpu"])
        self.assertEqual(scheduler.ready, ["t1"])

    def test_runtime_wraps_scheduler(self):
        runtime = Runtime()
        runtime.spawn("t1", ["cpu"])
        self.assertEqual(runtime.scheduler.stats()["ready"], ["t1"])


if __name__ == "__main__":
    unittest.main()
