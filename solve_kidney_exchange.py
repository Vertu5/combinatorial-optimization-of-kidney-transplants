from kidney_functions import *

def solve_kidney_exchange(filename, solve_cycles=False):
    # Read data from the CSV file
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

    if solve_cycles:

        print("Start solving for kidney exchange with cycle")

        C = []  # list of cycles

        while True:
            inside = False
            solution,obj = kydneys(graph, M, C, num_pairs)
            # Check solution's cycles exceed the maximum cycle length
            for cycle in form_chain_and_cycles(solution):
                if len(cycle) - 1 > 2*M:
                    C.append(cycle)
                    inside = True
                    
            if not inside:
                break

        print("end of solving for kidney exchange with cycle")
        print()
        print(f"Optimal solution with cycle length of maximum = {M}")
        print(f"The objective value is {obj}")
        formatted_assignment = []
        print(solution)
        for u, v in solution:
            if int(u) >= graph.number_of_nodes() // 2:
                formatted_assignment.append(f"Assign patient {int(u) - graph.number_of_nodes() // 2} to donor {int(v)}")
            else:
                formatted_assignment.append(f"Assign donor {int(u)} to patient {int(v) - graph.number_of_nodes() // 2}")
        
        print()
        print("Assignment")
        for assignment in formatted_assignment:
            print(assignment)
            
        print()

        return solution
    
    else :
        print("Start solving for kidney exchange")
        
        solution,obj = kydneys(graph, M, [], num_pairs)
        print("end of solving for kidney exchange")
        print()
        print(f"The objective value is {obj}")
        formatted_assignment = []
        print(solution)
        for u, v in solution:
            if int(u) >= graph.number_of_nodes() // 2:
                formatted_assignment.append(f"Assign patient {int(u) - graph.number_of_nodes() // 2} to donor {int(v)}")
            else:
                formatted_assignment.append(f"Assign donor {int(u)} to patient {int(v) - graph.number_of_nodes() // 2}")
        
        print()
        print("Assignment")
        for assignment in formatted_assignment:
            print(assignment)
            
        print()
        

