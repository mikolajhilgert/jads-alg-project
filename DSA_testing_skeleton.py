import sys 

class Graph:
    ''' Graph is composed of Adjacency lists and the target number of bins.
    Two bins should not be placed adjacent to each other.'''

    __slots__ = ["n", "m", "k", "adjacency_list"]

    def __init__(self, n, m, k) -> None:
        '''Initialise empty graph

        :param int n: Number of vertices
        :param int m: Number of edges
        :param int k: Target size of independent set
        '''
        self.n = n
        self.m = m
        self.k = k
        self.adjacency_list = [set() for _ in range(n)]

    @classmethod
    def from_file(cls, file_path) -> None:
        '''Loads a graph from a file

        :param str file_path: Path to graph input file
        '''
        with open(file_path, 'r') as f:
            # extract graph parameters
            m, n, k = map(int, f.readline().split())
            # call graph class constructor
            graph = cls(n, m, k)
            # skip whitespaces
            edges = [line for line in f if not line.isspace()]
            for edge in edges:
                # extract vertices connected by edge 
                u, v = map(int, edge.split())
                graph.add_edge(u-1, v-1)

        return graph
    
    @classmethod
    def parse_input(cls) -> None:
        '''
        NOTE: Enforcing constraints on input is not added as domains can change
        '''
        # Get number of streets, intersections and bins (respectively)
        m, n, k = sys.stdin.readline().split()
        graph = cls(int(n), int(m), int(k))

        # iterate over number of edges
        for _ in range(graph.m):
            u, v = map(int, input().split())
            graph.add_edge(u-1, v-1)

        return graph

    def add_edge(self, u, v) -> None:
        '''Adds an edge between vertex u and vertex v on the adjacency list

        :param int u: Vertex 1 index
        :param int v: Vertex 2 index
        '''
        self.adjacency_list[u].add(v)
        self.adjacency_list[v].add(u)

    def validate_number_of_bins(self) -> None:
        '''
        Validates number of bins on this graph

        input: None needed as its called on itself
        output: None, as it writes using stdout the result ('possible' or 'impossible')
        '''
        k = self.k
        n = self.n
        
        def backtrack(vertex, current_set):
            # Base case: if all vertices have been considered
            if vertex == n:
                # Check if the current set has reached the desired size
                return len(current_set) >= k

            # Include the current vertex in the set if it's non-adjacent to all vertices in the set
            if not self.adjacency_list[vertex] & current_set: 
                current_set.add(vertex)
                if backtrack(vertex + 1, current_set):
                    return True 
                current_set.remove(vertex)

            # Don't include the current vertex in the set
            if backtrack(vertex + 1, current_set):
                return True

            return False

        current_set = set()
        if backtrack(0, current_set):
            sys.stdout.write("possible")
        else:
            sys.stdout.write("impossible")
        
a_graph = Graph.parse_input()
a_graph.validate_number_of_bins()
