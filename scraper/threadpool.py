import page, settings, time
from threading import *
from queue import Queue, Empty

class Worker(Thread):
    def __init__(self, tasks, threadNumber):
        Thread.__init__(self)
        self.tasks = tasks
        self.threadNumber = threadNumber
        self.exitStatus = False
        self.done = Event()
        self.links = {
            "internal": [],
            "external": [],
            "mail": []
        }
        self.start()

    def run(self):
        while not self.exitStatus:
            try:
                task = self.tasks.get(block=False, timeout=0)
                p = page.Webpage(task)
                self.links = p.links
                # self.links.update({"internal" : p.links["internal"]})
                # self.links.update({"external" : p.links["external"]})
                # self.links.update({"mail" : p.links["mail"]})
            except Empty as e:
                pass

    def returnTasks(self, key="external"):
        return self.links[key]

    def exit(self):
        self.exitStatus = True

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
        time.sleep(0.5)
        for worker in self.workers:
            for task in worker.returnTasks():
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