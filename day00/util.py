import math

# From https://github.com/mcpower/adventofcode/blob/15ae109bc882ca688665f86e4ca2ba1770495bb4/utils.py
def min_max(l):
    return min(l), max(l)

# From https://stackoverflow.com/a/39644726
def get_digit(number, n):
    return number // 10**n % 10

def median(values):
    sorted_values = sorted(values)
    count = len(sorted_values)
    middle = count // 2
    if count % 2:
        return sorted_values[middle]
    else:
        return sum(sorted_values[middle - 1:middle + 1]) / 2

def init_grid(height, width, fill=None):
    grid = [[]] * (height)
    for y in range(height):
        grid[y] = [fill]*width
    return grid

def pretty_grid(array, xsep="", ysep="\n"):
    string_list = []
    for y in array:
        string_list.append(xsep.join([str(i) for i in y]))
    return ysep.join(string_list)

def between(x, a, b):
    return (a <= x <= b) or (b <= x <= a)

def to_unit_vector(vector):
    unit = []
    magnitude = math.sqrt( sum([x**2 for x in vector]) )
    for x in vector:
        unit.append(x/magnitude)
    return unit

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def from_iterable(point):
        return Point(point[0], point[1])

    def distance(self, other):
        return math.sqrt( (self.x - other.x)**2 + (self.y - other.y)**2 )

    def manhattan_distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def to_tuple(self):
        return (self.x, self.y)

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        else:
            return False

    def __str__(self):
        return "({0},{1})".format(self.x, self.y)

    def __hash__(self):
        return self.__str__().__hash__()

class LineSegment(object):
    def __init__(self, p1, p2):
        assert isinstance(p1, Point), "Argument should be a point"
        assert isinstance(p1, Point), "Argument should be a point"

        self.p1 = p1
        self.p2 = p2

    def slope(self):
        rise = (self.p2.y - self.p1.y)
        run = (self.p2.x - self.p1.x)

        if run == 0:
            return math.nan
        return rise/run

    def __str__(self):
        return "{0} -> {1}".format(self.p1, self.p2)

    def __hash__(self):
        return self.__str__().__hash__()

class Graph(object):

    def __init__(self):
        self.vertices = { }

    def add_vertex(self, vertex):
        if vertex not in self.vertices:
            self.vertices[vertex] = [ ]

    def add_edge(self, edge, weight=1, bidirectional=True):

        if edge[0] in self.vertices:
            self.vertices[edge[0]].append((edge[1],weight))
        else:
            self.vertices[edge[0]] = [ (edge[1],weight) ]

        if edge[1] not in self.vertices:
            self.vertices[edge[1]] = []

        if bidirectional:
            self.vertices[edge[1]].append( (edge[0],weight) )

    def neighbors(self, vertex):
        if vertex in self.vertices:
            return [x[0] for x in self.vertices[vertex]]
        else:
            return None

    def edge_weight(self, edge):
        if edge[0] not in self.vertices or edge[1] not in self.vertices:
            return None

        edges = self.vertices[edge[0]]
        for e in edges:
            if e[0] == edge[1]:
                return e[1]
        return None

    def dijkstra(self, source):
        if source not in self.vertices:
            return None

        vertices = set(self.vertices.keys())

        distance = { vertex:math.inf for vertex in vertices }
        previous = { vertex:None for vertex in vertices }
        distance[source] = 0

        while(len(vertices) > 0):
            distance_subset = { vertex:distance[vertex] for vertex in vertices }
            v = min(distance_subset, key=distance_subset.get)
            vertices.remove(v)

            for neighbor in [x for x in self.neighbors(v) if x in vertices]:
                new_distance = distance[v] + self.edge_weight([v,neighbor]) # Add weight
                if new_distance < distance[neighbor]:
                    distance[neighbor] = new_distance
                    previous[neighbor] = v

        return distance, previous

    def __str__(self):
        graph_str = []
        for vertex in self.vertices:
            graph_str.append(f'{vertex}: {self.vertices[vertex]}')
        return "\n".join(graph_str)
