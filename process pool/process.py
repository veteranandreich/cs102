from multiprocessing import Process, Queue, Manager
from heavy_func import sorter
import psutil


class ProcessPool:
    def __init__(self, min_workers=2, max_workers=10, mem_usage=1024):
        self.min_workers = min_workers
        self.max_workers = max_workers
        self.mem_usage = mem_usage
        self.process_ram = 0

    def mem_test(self, func, data):
        return_dict = Manager().dict()
        proc = Process(target=func, args=(data,))
        proc.start()
        proc1 = Process(target=self.measure_ram, args=(proc.pid, return_dict))
        proc1.start()
        proc.join()
        proc1.join()
        self.process_ram = return_dict['process_ram']

    def measure_ram(self, pid, return_dict):
        max_ram = 0
        try:
            while psutil.pid_exists(pid):
                result = psutil.Process(pid).memory_info().rss / 1024 ** 2
                if result > max_ram:
                    max_ram = result
        except psutil.NoSuchProcess:
            pass
        return_dict['process_ram'] = max_ram

    def map(self, func, bid_data: Queue):
        self.mem_test(func, bid_data.get())
        print(self.process_ram)
        process_amount = int(self.mem_usage / self.process_ram)
        print(process_amount)
        data_size = bid_data.qsize()
        print(data_size)
        procs = []
        if process_amount > self.max_workers:
            process_amount = self.max_workers
        elif process_amount < self.min_workers:
            raise Exception('Not enough RAM')
        for _ in range(process_amount):
            proc = Process(target=func, args=(bid_data.get(),))
            procs.append(proc)
            proc.start()
        while not bid_data.empty():
            for idx, proc in enumerate(procs):
                if not proc.is_alive():
                    new_proc = Process(target=func, args=(bid_data.get(),))
                    new_proc.start()
                    procs[idx] = new_proc
                    print('{0:.2f}%'.format(100 - (bid_data.qsize()/data_size) * 100))
        for proc in procs:
            proc.join()
        print('Done')
        return process_amount, self.process_ram


if __name__ == '__main__':
    pool = ProcessPool(2, 10, 1024)
    q = Queue()
    for _ in range(50):
        q.put(1)
    a, b = pool.map(sorter, q)
    print(a, b)
