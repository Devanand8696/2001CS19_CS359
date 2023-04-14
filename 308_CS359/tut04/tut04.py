from collections import defaultdict
from datetime import datetime
import threading
import time
import sys

# Require Variables
no_router = 0  # No. of Routers
routers = []  # Routers
links = defaultdict(list)  # Links between Routers
queues = {}  # Queue for Each Router

# Constant for Infinite Distance
INF = -1


# Router extends Thread
class Router(threading.Thread):
    def __init__(self, router, links):
        threading.Thread.__init__(self)
        self.router = router
        self.neighbors = {link[0]: int(link[1]) for link in links}

        # Set up Routing Table
        self.routing_table = {}
        for router in routers:
            if router == self.router:
                self.routing_table[router] = (0, [router])
            elif router in self.neighbors:
                self.routing_table[router] = (self.neighbors[router], [router])
            else:
                self.routing_table[router] = (INF, [])

        self.updated = defaultdict(lambda: 0)

    def run(self):
        self.iteration = 0
        while True:
            self.iteration += 1
            time.sleep(0.5)
            self.send()
            time.sleep(1)
            self.update()
            time.sleep(0.5)

    def send(self):
        for neighbor in self.neighbors:
            queues[neighbor].append((self.router, self.routing_table))

    def update(self):
        self.updated = defaultdict(lambda: 0)
        while queues[self.router]:
            sender, routing_table = queues[self.router].pop(0)
            for dest, (cost, hop) in routing_table.items():
                if cost == INF:
                    continue
                next = [sender] + (hop)
                if self.routing_table[dest][0] == INF:
                    self.routing_table[dest] = (self.neighbors[sender] + cost, next)
                    self.updated[dest] = 1
                elif self.routing_table[dest][0] > self.neighbors[sender] + cost:
                    self.routing_table[dest] = (self.neighbors[sender] + cost, next)
                    self.updated[dest] = 1


def printer(router_threads):
    iterations = 0
    while 1:
        print("Iteration: {}".format(iterations), end="\t")
        iterations += 1

        # Print Routing Tables
        for router in router_threads:
            print("Router: {}".format(router.router))
            print("Routing Table:", end="\t")
            for dest, (cost, hop) in router.routing_table.items():
                print(
                    f"{dest} : {cost}{'*' if router.updated[dest] else ''} {hop}",
                    end="\t",
                )
            print()
        print("\n===================\n")
        time.sleep(2)

def dvr():
    # Run Router Threads
    router_threads = []
    for router in routers:
        router_links = links[router]
        router_thread = Router(router, router_links)
        router_threads.append(router_thread)
        router_thread.start()

    # Run Printer Thread
    printer_thread = threading.Thread(target=printer, args=(router_threads,))
    printer_thread.start()

    # Join router threads
    for router_thread in router_threads:
        router_thread.join()

    # Join printer thread
    printer_thread.join()


if __name__ == "__main__":
    start_time = datetime.now()

    # Get Input
    lines = []
    with open("C:/Users/C M DEVANANAD/Dropbox/My PC (DESKTOP-3N6L9BI)/Downloads/topology.txt", "r") as f:
        lines = f.readlines()

    # Process Input
    no_router = int(lines[0].strip())
    routers = lines[1].strip().split()
    for line in lines[2:-1]:
        link = line.strip().split()
        links[link[0]].append((link[1], link[2]))
        links[link[1]].append((link[0], link[2]))

    queues = {router: [] for router in routers}

    # Run DVR
    dvr()

    # This shall be the last lines of the code.
    end_time = datetime.now()
    print("Duration of Program Execution: {}".format(end_time - start_time))