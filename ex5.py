# Topological sorting can be implemented using an algorithm seen in
# class. Which algorithm? Why?
# It can be implemented using DFS (Depth First Search). Since topological
# ordering is when for every edge the "from" node comes before the "to" node.
# DFS does this since when it visits a node, it goes as deep as possible before 
# coming back. A node is only fully explored after all the nodes it points to 
# have also been fully explored, this order when we read it in reverse gives us 
# the topological order.

class GraphNode:
    def __init__(self, data):
        self.data = data
class Graph:
    def __init__(self):
        self.adjacency_list = {}
    def addNode(self, data): # adds a key to the dict with an empty list
        node = GraphNode(data)
        self.adjacency_list[node] = []
        return node
    def removeNode(self, node):
        if node not in self.adjacency_list:
            raise ValueError("f{node} is not in the graph")

        neighbors_of_node = self.adjacency_list[node]
        for neighbor, weight in neighbors_of_node:
            current_neighbor_list = self.adjacency_list[neighbor]
            updated_neighbor_list = []
            for n, w in current_neighbor_list:
                if n is not node:
                    updated_neighbor_list.append((n, w))
            self.adjacency_list[neighbor] = updated_neighbor_list
        del self.adjacency_list[node] 
    def addEdge(self, n1, n2, weight):
        if n1 not in self.adjacency_list:
            raise ValueError(f"{n1} is not in the graph")
        if n2 not in self.adjacency_list:
            raise ValueError(f"{n2} is not in the graph")

        # avoiding duplicate edges
        if not self._hasEdge(n1, n2):
            self.adjacency_list[n1].append((n2, weight))  # n1 to n2
            self.adjacency_list[n2].append((n1, weight))  # n2 to n1 
    def removeEdge(self, n1, n2):
        if n1 not in self.adjacency_list:
            raise ValueError(f"{n1} is not in the graph")
        if n2 not in self.adjacency_list:
            raise ValueError(f"{n2} is not in the graph")

        current_neighbors_n1 = self.adjacency_list[n1]
        updated_neighhbors_n1 = []
        for n, w in current_neighbors_n1:
            if n is not n2:
                updated_neighhbors_n1.append((n, w))
        self.adjacency_list[n1] = updated_neighhbors_n1

        current_neighbors_n2 = self.adjacency_list[n2]
        updated_neighhbors_n2 = []
        for n, w in current_neighbors_n2:
            if n is not n1:
                updated_neighhbors_n2.append((n, w))
        self.adjacency_list[n2] = updated_neighhbors_n2
    
    def isDag(self): # returns True if the graph is a DAG (no cycles)
        # has 3 states per node
        # 0 - unvisited
        # 1 - currently visiting
        # 2 - done
        state = {}
        for node in self.adjacency_list:
            state[node] = 0
        def dfsCycleCheck(node):
            state[node] = 1 # we visit the node
            for n, w in self.adjacency_list[node]:
                if state[n] == 1: 
                    # we hit a node we are currently visitng cycle found
                    return True
                if state[n] == 0: # univisited so we go deeper
                    if dfsCycleCheck(n):
                        return True
            state[node] = 2 # done with this node
            return False
        for node in self.adjacency_list: # we run DFS for every unvisited node
            if state[node] == 0:
                if dfsCycleCheck(node):
                    return False # cycle found, not a DAG tho
        return True # no cycles found
    
    def topoSort(self):
        if not self.isDag():
            return None
        state = {}
        for node in self.adjacency_list:
            state[node] = 0
        finished = []

        def dfsTopo(node):
            state[node] = 1
            for n, w in self.adjacency_list[node]:
                if state[n] == 0: # unvisited so go deeper
                    dfsTopo(n)
            state[node] = 2 # all neighbors visited, node is done
            finished.append(node)
        for node in self.adjacency_list:
            if state[node] == 0:
                dfsTopo(node)
        finished.reverse() # we reverse the list
        return finished
