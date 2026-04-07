class GraphNode:
    def __init__(self, data):
        self.data = data



class UnionFind:
    def __init__(self, nodes):
        self.parent = {node: node for node in nodes}
        self.rank = {node: 0 for node in nodes}

    def find(self, node):
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])  
        return self.parent[node]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)

        if root_u == root_v:
            return False  

        if self.rank[root_u] > self.rank[root_v]:
            self.parent[root_v] = root_u
        elif self.rank[root_u] < self.rank[root_v]:
            self.parent[root_u] = root_v
        else:
            self.parent[root_v] = root_u
            self.rank[root_u] += 1

        return True


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

        self.adjacency_list[n1].append((n2, weight))
        self.adjacency_list[n2].append((n1, weight))


    def get_edges(self):
        edges = []
        seen = set()

        for u in self.adjacency_list:
            for v, w in self.adjacency_list[u]:
                if (v, u) not in seen:
                    edges.append((u, v, w))
                    seen.add((u, v))

        return edges


    def mst(self):
        mst_graph = Graph()

        node_map = {}
        for node in self.adjacency_list:
            node_map[node] = mst_graph.addNode(node.data)

        uf = UnionFind(self.adjacency_list.keys())

        edges = self.get_edges()
        edges.sort(key=lambda x: x[2]) 

        for u, v, w in edges:
            if uf.union(u, v):  
                mst_graph.addEdge(node_map[u], node_map[v], w)

        return mst_graph


if __name__ == "__main__":
    g = Graph()

    a = g.addNode("A")
    b = g.addNode("B")
    c = g.addNode("C")
    d = g.addNode("D")

    g.addEdge(a, b, 1)
    g.addEdge(a, c, 4)
    g.addEdge(b, d, 2)
    g.addEdge(c, d, 3)

    mst = g.mst()

    print("MST edges:")
    for node in mst.adjacency_list:
        for neighbor, weight in mst.adjacency_list[node]:
            print(node.data, "-", neighbor.data, ":", weight)