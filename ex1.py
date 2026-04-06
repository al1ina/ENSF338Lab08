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
    
    def importFromFile(self, file):
        # we want to parse a GraphViz DOT file which is in the format:
        # strict graph G {
        #   node1 -- node2 [weight=5];
        #   node2 -- node3;
        # }
        try:
            f = open(file, 'r') 
        except FileNotFoundError: # file doesn't exist
            return None
        
        found_header = False
        found_open_brace = False
        parsed_edges = []
        for line in f:
            line = line.strip()
            
            if not line: # skipping blank lines
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
            line = line[:-1].strip() # removing semicolon from end
            if "--" not in line:
                f.close()
                return None
            
            weight = 1   # default weight
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
        
        # build the graph
        self.adjacency_list = {}
        node_map = {}   # maps name (string) to GraphNode

        for node1, node2, weight in parsed_edges:

            # create nodes if they don't exist
            if node1 not in node_map:
                node_map[node1] = self.addNode(node1)
            if node2 not in node_map:
                node_map[node2] = self.addNode(node2)

            # connect them
            self.addEdge(node_map[node1], node_map[node2], weight)

        return self

    
