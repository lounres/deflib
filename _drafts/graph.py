import copy
import functools
from deflib.exceptions import LogicError


# Class of graphs TODO: Дописать класс графов
class Graph:
    def __init__(self, *edges, Oriented=False, MultipleEdges=False, Loops=False, ToNameVertexes=False, AutoCorrectMode=True):
        self.O = self.Ori = self.Oriented = Oriented
        self.ME = self.MultEdges = self.MultipleEdges = MultipleEdges
        self.L = self.Loops = Loops
        self.TNV = self.ToNameVert = self.ToNameVertexes = ToNameVertexes

        TempNames = {}
        TempVert = {}
        for edge in edges:
            if type(edge) in [str, int]:
                TempNames[edge] = TempNames.get(edge, len(TempNames))
            else:
                TempNames[edge[0]] = TempNames.get(edge[0], len(TempNames))
                TempNames[edge[1]] = TempNames.get(edge[1], len(TempNames))
                TempVert[TempNames[edge[0]]] = TempVert.get(TempNames[edge[0]], []) + [TempNames[edge[1]]]
        self.V = self.Vert = self.Vertexes = [functools.reduce(lambda arr, element: arr[:element] + [arr[element] + 1] + arr[element + 1:], TempVert.get(i, []), [0] * len(TempNames)) for i in range(len(TempNames))]
        if self.ToNameVertexes:
            self.OVN = self.OwnVertNames = self.OwmVertexesNames = {val: key for key, val in TempNames}
            self.ONN = self.OwnNamesNum = self.OwnNamesNumbers = TempNames
        if not self.Oriented:
            for i in range(len(self.V)):
                for j in range(i):
                    self.V[i][j] = self.V[j][i] = self.V[i][j] + self.V[j][i]
        if not self.MultEdges:
            for i in range(len(self.V)):
                for j in range(len(self.V)):
                    self.V[i][j] = 1 if self.V[i][j] else 0
        if not self.Loops:
            if AutoCorrectMode:
                for i in range(len(self.V)):
                    self.V[i][i] = 0
            else:
                for i in range(len(self.V)):
                    if self.V[i][i]:
                        raise LogicError('There is prohibited loop')

        self.refresh_Edges()

    def __copy__(self):
        G = Graph(Oriented=self.O, MultipleEdges=self.ME, Loops=self.L, ToNameVertexes=self.TNV)
        G.V += self.V
        G.E += self.E
        if self.TNV:
            G.OVN = G.OwnVertNames = G.OwmVertexesNames = self.OVN
            G.ONN = G.OwnNamesNum = G.OwnNamesNumbers = self.ONN
        return G

    def __deepcopy__(self, memodict={}):
        return copy.copy(self)

    def refresh_Edges(self):
        self.E = self.Edges = functools.reduce(lambda arr, mb_edge: arr + [mb_edge] * self.V[mb_edge[0]][mb_edge[1]], functools.reduce(lambda arr1, arr2: arr1 + arr2, [[(i, j) for j in range(len(self.V))] for i in range(len(self.V))], []), []) if self.Oriented else \
            functools.reduce(lambda arr, mb_edge: arr + [mb_edge] * self.V[mb_edge[0]][mb_edge[1]], functools.reduce(lambda arr1, arr2: arr1 + arr2, [[(j, i) for j in range(i + 1)] for i in range(len(self.V))], []), [])

    def refresh_Vertexes(self, AutoCorrectMode=True):
        TempNames = {}
        TempVert = {}
        for edge in self.V:
            if type(edge) in [str, int]:
                TempNames[edge] = TempNames.get(edge, len(TempNames))
            else:
                TempNames[edge[0]] = TempNames.get(edge[0], len(TempNames))
                TempNames[edge[1]] = TempNames.get(edge[1], len(TempNames))
                TempVert[TempNames[edge[0]]] = TempVert.get(TempNames[edge[0]], []) + [TempNames[edge[1]]]
        self.V = self.Vert = self.Vertexes = [functools.reduce(lambda arr, element: arr[:element] + [arr[element] + 1] + arr[element + 1:], TempVert.get(i, []), [0] * len(TempNames)) for i in range(len(TempNames))]
        if self.ToNameVertexes:
            self.OVN = self.OwnVertNames = self.OwmVertexesNames = {val: key for key, val in TempNames}
            self.ONN = self.OwnNamesNum = self.OwnNamesNumbers = TempNames
        if not self.Oriented:
            for i in range(len(self.V)):
                for j in range(i):
                    self.V[i][j] = self.V[j][i] = self.V[i][j] + self.V[j][i]
        if not self.MultEdges:
            for i in range(len(self.V)):
                for j in range(len(self.V)):
                    self.V[i][j] = 1 if self.V[i][j] else 0
        if not self.Loops:
            if AutoCorrectMode:
                for i in range(len(self.V)):
                    self.V[i][i] = 0
            else:
                for i in range(len(self.V)):
                    if self.V[i][i]:
                        raise LogicError('There is prohibited loop')

    def refresh_OwnNamesNumbers(self):
        self.ONN = self.OwnNamesNum = self.OwnNamesNumbers = {val: key for key, val in self.OVN}

    def shift_vertexes(self, *vertexes):
        for i in range(len(vertexes) - 1):
            self.V[vertexes[i]], self.V[vertexes[i + 1]] = self.V[vertexes[i + 1]], self.V[vertexes[i]]
        for v in self.V:
            for i in range(len(vertexes) - 1):
                v[vertexes[i]], v[vertexes[i + 1]] = v[vertexes[i + 1]], v[vertexes[i]]
        self.refresh_Edges()
        if self.TNV:
            Shift = {i:i for i in range(len(self.V))}
            for i in range(-len(vertexes), 0):
                Shift[vertexes[i]] = vertexes[i + 1]
            self.OVN = self.OwnVertNames = self.OwmVertexesNames = {i:self.OVN[Shift[i]] for i in range(len(self.V))}
            self.refresh_OwnNamesNumbers()

    #TODO: Сдвиг вершин перестановкой (биекцией)

    def get_undergraph(self, Vert):
        Vert = sorted(Vert)
        copied_self = copy.copy(self)
        copied_self.V = copied_self.Vert = copied_self.Vertex = list(map(lambda pair: pair[1], filter(lambda pair: pair[0] in Vert, enumerate(map(lambda v: list(map(lambda pair: pair[1], (filter(lambda pair: pair[0] in Vert, enumerate(v))))), copied_self.V)))))
        copied_self.refresh_Edges()
        if copied_self.TNV:
            copied_self.OVN = copied_self.OwnVertNames = copied_self.OwmVertexesNames = {i:copied_self.OVN[Vert[i]] for i in range(len(Vert))}
            copied_self.refresh_OwnNamesNumbers()
        return copied_self

    def pop_undergraph(self, Vert):
        Vert = sorted(Vert)
        for i in range(len(Vert)):
            vertexes = list(range(Vert[i], i-1, -1))
            for i in range(len(vertexes) - 1):
                self.V[vertexes[i]], self.V[vertexes[i + 1]] = self.V[vertexes[i + 1]], self.V[vertexes[i]]
            for v in self.V:
                for i in range(len(vertexes) - 1):
                    v[vertexes[i]], v[vertexes[i + 1]] = v[vertexes[i + 1]], v[vertexes[i]]
        copied_self = copy.copy(self)
        copied_self.V = list(map(lambda v: v[:len(Vert)], copied_self.V[:len(Vert)]))
        self.V = list(map(lambda v: v[len(Vert):], self.V[len(Vert):]))
        copied_self.refresh_Edges()
        self.refresh_Edges()
        if self.TNV:
            AntiVert = list(filter(lambda i: i not in Vert, range(len(self.V) + len(copied_self.V))))
            copied_self.OVN = copied_self.OwnVertNames = copied_self.OwmVertexesNames = {i:copied_self.OVN[Vert[i]] for i in range(len(copied_self.V))}
            self.OVN = self.OwnVertNames = self.OwmVertexesNames = {i:self.OVN[AntiVert[i]] for i in range(len(self.V))}
            copied_self.refresh_OwnNamesNumbers()
            self.refresh_OwnNamesNumbers()
        return copied_self

    def seperate_connected_components(self):
        if not len(self.V):
            return [self]
        to_check = {0}
        checked = [False] * len(self.V)
        while bool(to_check):
            now = to_check.pop()
            checked[now] = True
            to_check |= set(map(lambda pair: pair[0], filter(lambda pair: pair[1] and not checked[pair[0]], enumerate(self.V[now]))))
        if all(checked):
            return [self]
        copied_self = copy.copy(self)
        component = copied_self.pop_undergraph(list(map(lambda pair: pair[0], filter(lambda pair: pair[1], enumerate(checked)))))
        return [component] + copied_self.seperate_connected_components()

    def __eq__(self, other):
        def test_bij(bij):
            for i in range(len(self.V)):
                for j in range(len(self.V)):
                    if self.V[i][j] != other.V[bij[i]][bij[j]]:
                        return False
            return True

        bijes = all_bijections(set(range(len(self.V))), set(range(len(other.V))))
        if list(filter(test_bij, bijes)):
            return True
        else:
            return False

    def __bool__(self):
        return bool(self.E)

    def __int__(self):
        return len(self.E)