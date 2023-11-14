import csv
import copy
import networkx as nx
from utils import *

def find_positive_weight_cycle(graph):
    """
    Finds a positive weight cycle in the given graph using the Floyd-Warshall algorithm.

    Args:
        graph (networkx.DiGraph): The input graph.

    Returns:
        cycle (list): List of edges forming the positive weight cycle.
            Returns None if no positive weight cycle is found.
    """
    cycle = list()

    dist = [[float('inf') if j != i else 0 for i in range(graph.number_of_nodes())]
            for j in range(graph.number_of_nodes())]

    parent = [[0 for _ in range(graph.number_of_nodes())] for _ in range(graph.number_of_nodes())]

    for u, v in graph.edges:
        dist[u][v] = -graph[u][v]['weight']
        parent[u][v] = u

    for w in range(graph.number_of_nodes()):
        for u in range(graph.number_of_nodes()):
            for v in range(graph.number_of_nodes()):
                if dist[u][v] > dist[u][w] + dist[w][v]:
                    dist[u][v] = dist[u][w] + dist[w][v]
                    parent[u][v] = parent[w][v]

                if u == v and dist[u][u] < 0:
                    while True:
                        w = parent[u][v]
                        cycle.append((w, v))
                        v = w
                        if v == u:
                            break

                    return cycle

    return None

def update_assignment(current_assignment, cycle, graph):
    new_assignment = []

    sorted_edges = []
    for u, v in cycle:
        weight = graph[u][v]['weight']
        if weight == 0:
            sorted_edges.append((u, v) if u > v else (v, u))
        else:
            sorted_edges.append((u, v) if u < v else (v, u))

    for edge in current_assignment:
        if edge in sorted_edges:
            sorted_edges.remove(edge)
        else:
            new_assignment.append(edge)

    new_assignment.extend(sorted_edges)

    return new_assignment

def solver(graph):
    
    current_assignment = []
    current_graph = nx.DiGraph(graph)

    while True:
        cycle = find_positive_weight_cycle(current_graph)
        if cycle is None:
            break

        current_assignment = update_assignment(current_assignment, cycle, current_graph)
        
        current_graph = nx.DiGraph()
        for u, v in graph.edges:
            if (u, v) not in current_assignment:
                current_graph.add_edge(u, v, weight=graph[u][v]['weight'])

        for u, v in current_assignment:
            current_graph.add_edge(v, u, weight=-graph[u][v]['weight']) 
        
    formatted_assignment = []
    for u, v in current_assignment:
        if u >= graph.number_of_nodes() // 2:
            formatted_assignment.append(f"Assign patient {u - graph.number_of_nodes() // 2} to donor {v}")
        else:
            formatted_assignment.append(f"Assign donor {u} to patient {v - graph.number_of_nodes() // 2}")
    
    return current_assignment, formatted_assignment
