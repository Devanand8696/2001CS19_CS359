from collections import defaultdict
from queue import PriorityQueue
from datetime import datetime
import threading
import time
from copy import deepcopy
import sys

# Require Variables
no_router = 0  # No. of Routers
routers = []  # Routers
links = defaultdict(list)  # Links between Routers
queues = {}  # Queue for Each Router

# Constant for Infinite Distance
INF = sys.maxsize


# Router extends Thread
class Router(threading.Thread):
    def __init__(self, router, links):
        threading.Thread.__init__(self)

        # Self Info
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

        # Update Record:  For * in printing
        self.updated = defaultdict(lambda: 0)

    # Thread Run Function
    def run(self):
        self.send()  # Send Table
        time.sleep(0.5)
        self.update()  # Update Table

    # Function to send update tables
    def send(self):
        for router in routers:
            queues[router].append((self.router, deepcopy(self.neighbors)))

    # Function to update table
    def update(self):
        # Create Global Network
        network = defaultdict(list)
        for router, neighbors in queues[self.router]:
            for neighbor, value in neighbors.items():
                network[router].append((neighbor, value))

        # Update Routing Table using Dijkstra's
        self.routing_table = dijkstra(network, self.router)
        pass


def dijkstra(network, start):
    dis = defaultdict(lambda: INF)
    visited = defaultdict(lambda: False)
    parent = defaultdict(lambda: None)

    dis[start] = 0

    pq = PriorityQueue()
    pq.put((0, start))

    while not pq.empty():
        (dist, cur) = pq.get()
        visited[cur] = True

        for neighbor, value in network[cur]:
            if not visited[neighbor]:
                if dis[neighbor] > dist + value:
                    dis[neighbor] = dist + value
                    parent[neighbor] = cur
                    pq.put((dis[neighbor], neighbor))

    # Create Routing Table
    routing_table = {}
    for router in routers:
        # Get Parent
        par = parent[router]
        paths = [router]
        while par:
            paths.append(par)
            par = parent[par]
        if paths:
            paths = list(reversed(paths))
            paths = paths[1:]

        routing_table[router] = (dis[router], paths)

    return routing_table


# Function to print data
def printer(router_threads):
    iterations = 0
    while iterations < 2:
        # Print Iteration
        print("Iteration: {}".format(iterations), end="\t")
        iterations += 1

        # Print Routing Tables
        for router in router_threads:
            print("Router: {}".format(router.router))
            print("Routing Table:", end="\t")
            for dest, (cost, hop) in router.routing_table.items():
                print(
                    f"{dest} : {cost if cost != INF else 'INF'}{'*' if router.updated[dest] else ''} {hop}",
                    end="\t",
                )
            print()
        print("\n===================\n")
        time.sleep(2)


def lsr():
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

    for rt in router_threads:
        rt.join()
    printer_thread.join()


if __name__ == "__main__":
    start_time = datetime.now()

    # Get Input
    lines = []
    with open("topology.txt", "r") as f:
        lines = f.readlines()

    # Process Input
    no_router = int(lines[0].strip())
    routers = lines[1].strip().split()
    for line in lines[2:-1]:
        link = line.strip().split()
        links[link[0]].append((link[1], link[2]))
        links[link[1]].append((link[0], link[2]))

    queues = {router: [] for router in routers}

    lsr()

    end_time = datetime.now()
    print("Duration of Program Execution: {}".format(end_time - start_time))
