import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import itertools
import numpy as np

# Membuat graf 4 node/titik lokasi
G = nx.Graph()
G.add_nodes_from(['TULT', 'TUCH', 'OpenLibrary', 'Gd. Cacuk'])
G.add_edges_from([('TULT', 'TUCH'), ('TULT', 'OpenLibrary'), ('TULT', 'Gd. Cacuk'), ('TUCH', 'OpenLibrary'), ('TUCH', 'Gd. Cacuk'), ('OpenLibrary', 'Gd. Cacuk')])

# Jarak antar lokasi
distance_dict = {
    ('TULT', 'TUCH'): 500,
    ('TULT', 'OpenLibrary'): 650,
    ('TULT', 'Gd. Cacuk'): 950,
    ('TUCH', 'OpenLibrary'): 160,
    ('TUCH', 'Gd. Cacuk'): 600,
    ('OpenLibrary', 'Gd. Cacuk'): 900
}

# Konversi jarak tadi menjadi matriks
nodes = list(G.nodes)
node_index = {node: idx for idx, node in enumerate(nodes)}
n = len(nodes)
graph = np.full((n, n), np.inf)
for (node1, node2), dist in distance_dict.items():
    i, j = node_index[node1], node_index[node2]
    graph[i, j] = graph[j, i] = dist

# Metode Brute Force
def tsp(graph, start_idx):
    V = len(graph)
    vertex = [i for i in range(V) if i != start_idx]
    min_cost = float('inf')
    min_path = []

    for perm in itertools.permutations(vertex):
        current_cost = 0
        k = start_idx
        for j in perm:
            current_cost += graph[k][j]
            k = j
        current_cost += graph[k][start_idx]

        if current_cost < min_cost:
            min_cost = current_cost
            min_path = [start_idx] + list(perm)

    return [nodes[i] for i in min_path], int(min_cost)

# Metode Greedy
def greedy(start_node):
    graph_dict = {
        'TULT': {'TUCH': 500, 'OpenLibrary': 650, 'Gd. Cacuk': 950},
        'TUCH': {'TULT': 500, 'OpenLibrary': 160, 'Gd. Cacuk': 600},
        'OpenLibrary': {'TULT': 650, 'TUCH': 160, 'Gd. Cacuk': 900},
        'Gd. Cacuk': {'TULT': 950, 'TUCH': 600, 'OpenLibrary': 900}
    }

    nodes = list(G.nodes)
    nodes.remove(start_node)
    path = [start_node]
    while nodes:
        next_node = min(nodes, key=lambda node: graph_dict[path[-1]][node])
        path.append(next_node)
        nodes.remove(next_node)
    path.append(start_node)
    total_dist = sum(graph_dict[path[i]][path[i + 1]] for i in range(len(path) - 1))
    return path, int(total_dist)

# Desain UI
st.title("Tel-U Students Problem")
start_node = st.selectbox("Ingin mulai dari mana?", ["TULT", "TUCH", "OpenLibrary", "Gd. Cacuk"])
method = st.selectbox("Pilih metode:", ["Brute Force", "Greedy"])

if st.button("Mulai"):
    start_idx = node_index[start_node]
    if method == "Brute Force":
        path, distance = tsp(graph, start_idx)
    else:
        path, distance = greedy(start_node)
    st.write("Rute:", path)
    st.write("Total jarak:", distance)

    # Create a new graph for the route
    route_G = nx.Graph()
    route_G.add_nodes_from(path)
    for i in range(len(path) - 1):
        route_G.add_edge(path[i], path[i + 1])
    route_G.add_edge(path[-1], path[0])  # Complete the circuit

    # Define fixed positions for nodes
    pos = {
        'TULT': (0, 1),
        'TUCH': (1, 1),
        'OpenLibrary': (1, 0),
        'Gd. Cacuk': (0, 0)
    }

    nx.draw_networkx(route_G, pos, node_color='r', edge_color='black', with_labels=True)
    plt.axis('off')
    st.pyplot(plt)
