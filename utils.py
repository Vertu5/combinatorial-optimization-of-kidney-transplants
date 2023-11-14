import csv
import copy
import networkx as nx

def preprocess_data(filename):
    """
    Preprocesses a CSV file containing weights and constructs a directed graph.

    Args:
        filename (str): The name of the CSV file.

    Returns:
        graph (networkx.DiGraph): The constructed directed graph.
    """
    weights = {}
    is_header = True

    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if is_header:
                is_header = False
                num_pairs = int(row[0])
                num_links = int(row[1])
                M = int(row[2])
                continue
            weights[("d" + str(int(row[0]))), ("p" + str(int(row[1])))] = float(row[2])

    # Create an empty graph
    graph = nx.DiGraph()

    # Traverse the weights dictionary
    for (d, p), weight in weights.items():
        donor_num = int(d[1:])
        patient_num = int(p[1:]) + num_pairs

        # Add the edge to the graph with the corresponding weight
        graph.add_edge(donor_num, patient_num, weight=weight)

    for i in range(num_pairs):
        graph.add_edge(i + num_pairs, i, weight=0.0)

    return graph, M