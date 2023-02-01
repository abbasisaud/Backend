class Graph:
    def __init__(self, nodes, init_graph):
        self.nodes = nodes
        self.graph = self.construct_graph(nodes, init_graph)

    def construct_graph(self, nodes, init_graph):
        graph = {}
        for node in nodes:
            graph[node] = {}
        
        graph.update(init_graph)
        
        for node, edges in graph.items():
            for adjacent_node, value in edges.items():
                if graph[adjacent_node].get(node, False) == False:
                    graph[adjacent_node][node] = value
                    
        return graph
    
    def add_edge(self, u, v, w):
        self.graph[u][v] = w
 
    def printAllPathsUtil(self, u, d, visited, path, dist, paths_distances, graph):
        visited[u]= True
        path.append(u)

        for v, w in graph[u].items():
            if visited[v]==False:
                self.printAllPathsUtil(v, d, visited, path, dist+w, paths_distances, graph)

        if u == d:
            paths_distances.append((path[:], dist))

        path.pop()
        visited[u]= False

    def printAllPaths(self, s, d):
        visited = {node: False for node in self.nodes}
        paths = []
        path = []
        dist = 0
        paths_distances = []
        self.printAllPathsUtil(s, d, visited, path, dist, paths_distances, self.graph)

        paths_distances.sort(key=lambda x: x[1])
        for path, distance in paths_distances:
            paths.append(path)
            paths.append(distance)
        return paths

nodes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
def create_init_graph(nodes, edges):
    init_graph = {}
    for node in nodes:
        init_graph[node] = {}
    
    for edge in edges:
        u, v, w = edge
        init_graph[u][v] = w
        
    return init_graph
edges = [
    ('a', 'b', 2), 
    ('a', 'c', 3), 
    ('a', 'd', 1), 
    ('b', 'd', 4), 
    ('b', 'e', 5), 
    ('c', 'd', 2), 
    ('c', 'f', 7), 
    ('d', 'g', 1),
    ('e', 'h', 3),
    ('f', 'h', 8),
    ('g', 'h', 2)
]

init_graph = create_init_graph(nodes, edges)
g = Graph(nodes, init_graph)

def truncate_list(paths, length):
    for element in paths:
        if type(element) == int:
            paths.remove(element)
    while len(paths) > length:
        del paths[-1]
    return paths


