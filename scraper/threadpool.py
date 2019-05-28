import page, settings
from threading import *
from queue import Queue, Empty

class Worker(Thread):
    def __init__(self, tasks, threadNumber):
        Thread.__init__(self)
        self.tasks = tasks
        self.threadNumber = threadNumber
        self.exit_status = False
        self.done = Event()
        self.links = {
            "internal": [],
            "external": [],
            "mail": []
        }
        self.start()

    def run(self):
        while not self.exit_status:
            try:
                task = self.tasks.get(block=False, timeout=1)
                p = page.Webpage(task)
                self.links.update({"internal" : p.links["external"]})
            except Empty as e:
                pass

    def returnTasks(self, key="external"):
        return self.links[key]

    def exit(self):
        self.exit_status = True

class ThreadPool:
    def __init__(self, args, tasks=[]):
        self.depth = args.depth
        self.num_threads = args.threads
        self.workers = []
        self.done = False

        self.tasks = Queue(self.num_threads)
        self.init(self.num_threads)
        
        for task in tasks:
            self.tasks.put(task)
        self.iterate()

    def init(self, num_threads):
        for i in range(num_threads):
            self.workers.append(Worker(self.tasks, i))

    def addTasks(self):
        for worker in self.workers:
            tasks = worker.returnTasks()
            for task in tasks:
                self.tasks.put(task)

    def closeThreads(self):
        for worker in self.workers:
            worker.exit()
        self.workers = []

    def iterate(self):
        while self.depth != 0:
            self.addTasks()
            self.depth -= 1
            if self.tasks.empty():
                self.closeThreads()