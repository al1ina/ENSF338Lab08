# Q1 ANSWER:
# Two queue implementations are using a simple list with linear search to find the minimum distance node, 
# which is inefficient with (O(V^2)) time complexity, and using a min-heap (priority queue), 
# which is more efficient with (O((V + E)\log V)) time complexity.


import heapq
import time
import random
import matplotlib.pyplot as plt


class GraphNode:
    def __init__(self, data):
        self.data = data


class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def addNode(self, data):
        node = GraphNode(data)
        self.adjacency_list[node] = []
        return node

    def addEdge(self, n1, n2, weight):
        if n1 not in self.adjacency_list or n2 not in self.adjacency_list:
            raise ValueError("Node not in graph")

        if not self._hasEdge(n1, n2):
            self.adjacency_list[n1].append((n2, weight))
            self.adjacency_list[n2].append((n1, weight))

    def _hasEdge(self, n1, n2):
        return any(neighbor == n2 for neighbor, _ in self.adjacency_list[n1])

    def importFromFile(self, file):
        try:
            f = open(file, 'r')
        except FileNotFoundError:
            return None

        found_header = False
        found_open_brace = False
        parsed_edges = []

        for line in f:
            line = line.strip()
            if not line:
                continue

            if not found_header:
                if line.lower().startswith("strict graph"):
                    found_header = True
                    if "{" in line:
                        found_open_brace = True
                    continue
                else:
                    f.close()
                    return None

            if line == "}":
                break

            if not line.endswith(";"):
                f.close()
                return None

            line = line[:-1].strip()

            if "--" not in line:
                f.close()
                return None

            weight = 1
            if "[" in line:
                parts = line.split("[")
                node_part = parts[0].strip()
                weight_part = parts[1].replace("]", "").strip()

                weight_sides = weight_part.split("=")
                weight = int(weight_sides[1].strip())
            else:
                node_part = line

            node1, node2 = node_part.split("--")
            node1 = node1.strip()
            node2 = node2.strip()

            parsed_edges.append((node1, node2, weight))

        f.close()

        self.adjacency_list = {}
        node_map = {}

        for n1, n2, w in parsed_edges:
            if n1 not in node_map:
                node_map[n1] = self.addNode(n1)
            if n2 not in node_map:
                node_map[n2] = self.addNode(n2)

            self.addEdge(node_map[n1], node_map[n2], w)

        return self

    # Slow dijkstra
    def slowSP(self, start):
        dist = {node: float('inf') for node in self.adjacency_list}
        dist[start] = 0
        visited = set()

        while len(visited) < len(self.adjacency_list):
            min_node = None
            min_dist = float('inf')

            for node in self.adjacency_list:
                if node not in visited and dist[node] < min_dist:
                    min_dist = dist[node]
                    min_node = node

            if min_node is None:
                break

            visited.add(min_node)

            for neighbor, weight in self.adjacency_list[min_node]:
                if dist[min_node] + weight < dist[neighbor]:
                    dist[neighbor] = dist[min_node] + weight

        return dist


    # Fast dijkstra using a heap
    def fastSP(self, start):
        dist = {node: float('inf') for node in self.adjacency_list}
        dist[start] = 0

        pq = [(0, id(start), start)]

        while pq:
            current_dist, _, node = heapq.heappop(pq)

            if current_dist > dist[node]:
                continue

            for neighbor, weight in self.adjacency_list[node]:
                new_dist = current_dist + weight
                if new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    heapq.heappush(pq, (new_dist, id(neighbor), neighbor))

        return dist


def measure_performance(graph):
    slow_times = []
    fast_times = []

    nodes = list(graph.adjacency_list.keys())

    # sample to avoid huge runtime
    sample_nodes = random.sample(nodes, min(30, len(nodes)))

    for node in sample_nodes:
        start = time.perf_counter()
        graph.slowSP(node)
        slow_times.append(time.perf_counter() - start)

        start = time.perf_counter()
        graph.fastSP(node)
        fast_times.append(time.perf_counter() - start)

    def stats(times):
        return min(times), max(times), sum(times) / len(times)

    print("SLOW (min, max, avg):", stats(slow_times))
    print("FAST (min, max, avg):", stats(fast_times))

    # histogram
    plt.hist(slow_times, alpha=0.5, label="Slow")
    plt.hist(fast_times, alpha=0.5, label="Fast")
    plt.legend()
    plt.title("Execution Time Distribution")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Frequency")
    plt.show()


if __name__ == "__main__":
    g = Graph()
    g.importFromFile("random.dot")
    measure_performance(g)



# Q4 ANSWER:

# The fast implementation using a heap is much faster than the slow implementation.

# This is because the slow version performs a linear scan to find the minimum distance node at each step,
# leading to O(V^2) complexity, which becomes very slow for large graphs.

# The fast version uses a priority queue through a heap, reducing the complexity to
# O((V + E) log V), which scales much better.
# As shown on the histogram, the execution times for the slow implementation are much larger and more widely distributed,
# while the fast implementation has much smaller and tightly clustered execution times.
