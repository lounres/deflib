from .graph import Graph
import functools


# Another initializer of graph() TODO: Написать инициализатор, а не...
def graph_by_table(Table, Oriented=False, MultipleEdges=False, Loops=False, ToNameVertexes=False, AutoCorrectMode=True):
    return Graph(functools.reduce(lambda arr, mb_edge: arr + [mb_edge] * Table[mb_edge[0]][mb_edge[1]], functools.reduce(lambda arr1, arr2: arr1 + arr2, [[(i, j) for j in range(len(Table))] for i in range(len(Table))], []), []), Oriented, MultipleEdges, Loops, ToNameVertexes, AutoCorrectMode)
