import time


class GraphNode:
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return str(self.data)


class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def addNode(self, data):
        node = GraphNode(data)
        self.adjacency_list[node] = []
        return node

    def removeNode(self, node):
        if node not in self.adjacency_list:
            raise ValueError(f"{node} is not in the graph")

        neighbors_of_node = self.adjacency_list[node]
        for neighbor, weight in neighbors_of_node:
            current_neighbor_list = self.adjacency_list[neighbor]
            updated_neighbor_list = []

            for n, w in current_neighbor_list:
                if n is not node:
                    updated_neighbor_list.append((n, w))

            self.adjacency_list[neighbor] = updated_neighbor_list

        del self.adjacency_list[node]

    def _hasEdge(self, n1, n2):
        for neighbor, weight in self.adjacency_list[n1]:
            if neighbor is n2:
                return True
        return False

    def addEdge(self, n1, n2, weight):
        if n1 not in self.adjacency_list:
            raise ValueError(f"{n1} is not in the graph")
        if n2 not in self.adjacency_list:
            raise ValueError(f"{n2} is not in the graph")

        if not self._hasEdge(n1, n2):
            self.adjacency_list[n1].append((n2, weight))
            self.adjacency_list[n2].append((n1, weight))

    def removeEdge(self, n1, n2):
        if n1 not in self.adjacency_list:
            raise ValueError(f"{n1} is not in the graph")
        if n2 not in self.adjacency_list:
            raise ValueError(f"{n2} is not in the graph")

        current_neighbors_n1 = self.adjacency_list[n1]
        updated_neighbors_n1 = []
        for n, w in current_neighbors_n1:
            if n is not n2:
                updated_neighbors_n1.append((n, w))
        self.adjacency_list[n1] = updated_neighbors_n1

        current_neighbors_n2 = self.adjacency_list[n2]
        updated_neighbors_n2 = []
        for n, w in current_neighbors_n2:
            if n is not n1:
                updated_neighbors_n2.append((n, w))
        self.adjacency_list[n2] = updated_neighbors_n2

    def importFromFile(self, file):
        try:
            f = open(file, "r")
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
                if "]" not in line:
                    f.close()
                    return None

                parts = line.split("[")
                node_part = parts[0].strip()
                weight_part = parts[1].replace("]", "").strip()

                if "=" not in weight_part:
                    f.close()
                    return None

                weight_sides = weight_part.split("=")
                if weight_sides[0].strip() != "weight":
                    f.close()
                    return None

                try:
                    weight = int(weight_sides[1].strip())
                except ValueError:
                    f.close()
                    return None
            else:
                node_part = line

            node_sides = node_part.split("--")
            if len(node_sides) != 2:
                f.close()
                return None

            node1 = node_sides[0].strip()
            node2 = node_sides[1].strip()

            if not node1 or not node2:
                f.close()
                return None

            parsed_edges.append((node1, node2, weight))

        f.close()

        if not found_header or not found_open_brace:
            return None

        self.adjacency_list = {}
        node_map = {}

        for node1, node2, weight in parsed_edges:
            if node1 not in node_map:
                node_map[node1] = self.addNode(node1)
            if node2 not in node_map:
                node_map[node2] = self.addNode(node2)

            self.addEdge(node_map[node1], node_map[node2], weight)

        return self

    def dfs(self, start_node):
        if start_node not in self.adjacency_list:
            raise ValueError(f"{start_node} is not in the graph")

        visited = set()
        order = []

        def _dfs(node):
            visited.add(node)
            order.append(node)

            neighbors = []
            for neighbor, weight in self.adjacency_list[node]:
                neighbors.append(neighbor)

            neighbors.sort(key=lambda n: int(n.data))   
            for neighbor in neighbors:
                if neighbor not in visited:
                    _dfs(neighbor)

        _dfs(start_node)
        return order


class Graph2:
    def __init__(self):
        self.nodes = []
        self.adjacency_matrix = []

    def addNode(self, data):
        node = GraphNode(data)
        self.nodes.append(node)

        for row in self.adjacency_matrix:
            row.append(0)

        self.adjacency_matrix.append([0] * len(self.nodes))
        return node

    def removeNode(self, node):
        if node not in self.nodes:
            raise ValueError(f"{node} is not in the graph")

        index = self.nodes.index(node)

        del self.nodes[index]
        del self.adjacency_matrix[index]

        for row in self.adjacency_matrix:
            del row[index]

    def addEdge(self, n1, n2, weight):
        if n1 not in self.nodes:
            raise ValueError(f"{n1} is not in the graph")
        if n2 not in self.nodes:
            raise ValueError(f"{n2} is not in the graph")

        i = self.nodes.index(n1)
        j = self.nodes.index(n2)

        self.adjacency_matrix[i][j] = weight
        self.adjacency_matrix[j][i] = weight

    def removeEdge(self, n1, n2):
        if n1 not in self.nodes:
            raise ValueError(f"{n1} is not in the graph")
        if n2 not in self.nodes:
            raise ValueError(f"{n2} is not in the graph")

        i = self.nodes.index(n1)
        j = self.nodes.index(n2)

        self.adjacency_matrix[i][j] = 0
        self.adjacency_matrix[j][i] = 0

    def importFromFile(self, file):
        try:
            f = open(file, "r")
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
                if "]" not in line:
                    f.close()
                    return None

                parts = line.split("[")
                node_part = parts[0].strip()
                weight_part = parts[1].replace("]", "").strip()

                if "=" not in weight_part:
                    f.close()
                    return None

                weight_sides = weight_part.split("=")
                if weight_sides[0].strip() != "weight":
                    f.close()
                    return None

                try:
                    weight = int(weight_sides[1].strip())
                except ValueError:
                    f.close()
                    return None
            else:
                node_part = line

            node_sides = node_part.split("--")
            if len(node_sides) != 2:
                f.close()
                return None

            node1 = node_sides[0].strip()
            node2 = node_sides[1].strip()

            if not node1 or not node2:
                f.close()
                return None

            parsed_edges.append((node1, node2, weight))

        f.close()

        if not found_header or not found_open_brace:
            return None

        self.nodes = []
        self.adjacency_matrix = []
        node_map = {}

        for node1, node2, weight in parsed_edges:
            if node1 not in node_map:
                node_map[node1] = self.addNode(node1)
            if node2 not in node_map:
                node_map[node2] = self.addNode(node2)

            self.addEdge(node_map[node1], node_map[node2], weight)

        return self

    def dfs(self, start_node):
        if start_node not in self.nodes:
            raise ValueError(f"{start_node} is not in the graph")

        visited = set()
        order = []

        def _dfs(node):
            visited.add(node)
            order.append(node)

            i = self.nodes.index(node)
            neighbors = []

            for j in range(len(self.nodes)):
                if self.adjacency_matrix[i][j] != 0:
                    neighbors.append(self.nodes[j])

            neighbors.sort(key=lambda n: int(n.data))   

            for neighbor in neighbors:
                if neighbor not in visited:
                    _dfs(neighbor)

        _dfs(start_node)
        return order

    def printMatrix(self):
        print("Adjacency Matrix:")
        for row in self.adjacency_matrix:
            print(row)


def measure_dfs(graph, start_node, label):
    times = []

    for _ in range(10):
        start = time.perf_counter()
        dfs_order = graph.dfs(start_node)
        end = time.perf_counter()
        times.append(end - start)

    print(f"\n{label}")
    print("DFS order:", [node.data for node in dfs_order])
    print("Minimum time:", min(times))
    print("Maximum time:", max(times))
    print("Average time:", sum(times) / len(times))


if __name__ == "__main__":
    filename = "random.dot"

    # Graph using adjacency list
    g1 = Graph()
    if g1.importFromFile(filename) is None:
        print("Error: could not load graph into Graph from file.")
    else:
        start_node_g1 = next(iter(g1.adjacency_list))
        measure_dfs(g1, start_node_g1, "Graph (Adjacency List)")

    # Graph2 using adjacency matrix
    g2 = Graph2()
    if g2.importFromFile(filename) is None:
        print("Error: could not load graph into Graph2 from file.")
    else:
        start_node_g2 = g2.nodes[0]
        measure_dfs(g2, start_node_g2, "Graph2 (Adjacency Matrix)")

#The adjacency list version was much faster than the adjacency matrix version. 
#This is expected because adjacency lists only iterate through real neighbors,
# while adjacency matrices must scan entire rows. 
