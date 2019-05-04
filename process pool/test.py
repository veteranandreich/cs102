import unittest
from process import ProcessPool
import random
from queue import Queue


class MyTestCase(unittest.TestCase):
    def generate_data(self, len_q, len_list):
        q = Queue()
        for _ in range(len_q):
            array = [random.randint(0, 1) for _ in range(len_list)]
            q.put(array)
        return q

    def task(self, data):
        data.sort()

    def test_count_worker(self):
        worker = ProcessPool()
        self.assertEqual(10, worker.map(self.task, self.generate_data(30, 100000))[0])

    def test_count_worker_max(self):
        worker = ProcessPool(1, 2, 512)
        self.assertEqual(2, worker.map(self.task, self.generate_data(30, 100000))[0])

    def test_count_worker_min(self):
        worker = ProcessPool(15, 20, 512)
        self.assertRaisesRegex(Exception, "Not enough RAM", worker.map, self.task, self.generate_data(30, 100000))

    def test_memory(self):
        worker = ProcessPool()
        self.assertLessEqual(int(worker.map(self.task, self.generate_data(30, 100000))[1]), 37)

    def test_max_memory(self):
        worker = ProcessPool(1, 10, 500)
        count_worker = worker.map(self.task, self.generate_data(30, 100000))[0]
        mem_for_worker = worker.map(self.task, self.generate_data(30, 100000))[1]
        self.assertLessEqual(count_worker * mem_for_worker, 500)


if __name__ == '__main__':
    unittest.main()
