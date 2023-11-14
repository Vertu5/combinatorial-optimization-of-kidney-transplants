import networkx as nx
import matplotlib.pyplot as plt

def draw_donation_cycle_graph(cycles, weights):
    for cycle in cycles:
        donation_edges = []
        donneurs = [cycle[i] for i in range(len(cycle)) if i % 2 == 0]
        patients = [cycle[i] for i in range(len(cycle)) if i % 2 == 1]

        donneurs_set = set(donneurs)
        patients_set = set(patients)

        G = nx.DiGraph()

        for donneur in donneurs_set:
            G.add_node("D{}".format(donneur[1:]), color='red')

        for patient in patients_set:
            G.add_node("P{}".format(patient[1:]), color='green')

        for i in range(len(donneurs) - 1):
            donneur = donneurs[i]
            patient = patients[i]
            weight = weights[int(donneur[1:]), int(patient[1:])]
            donation_edges.append(("D{}".format(donneur[1:]), "P{}".format(patient[1:]), weight))
            donation_edges.append(("P{}".format(patient[1:]), "D{}".format(patient[1:]), 0))

        G.add_weighted_edges_from(donation_edges)

        edge_labels = nx.get_edge_attributes(G, 'weight')
        node_colors = [G.nodes[node]['color'] for node in G.nodes]

        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=500)
        nx.draw_networkx_edges(G, pos, width=2.0, arrowstyle='->', arrowsize=10)
        nx.draw_networkx_labels(G, pos)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12)

        plt.title("Cycle {}".format(cycle))
        plt.axis('off')
        plt.show()