import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

edges = [
    ('A','B',22), ('A','C',9), ('A','D',12),
    ('B','C',35), ('B','E',34), ('B','F',36),
    ('C','D',4), ('C','E',65), ('C','F',42),
    ('D','E',33), ('D','I',30),
    ('E','F',18), ('E','G',23), ('F','G',39), ('F','H',24),
    ('G','H',25), ('G','I',21), ('H','I',19)
]

G.add_weighted_edges_from(edges)

start_node = 'A'
distances = nx.single_source_dijkstra_path_length(G, start_node)
paths = nx.single_source_dijkstra_path(G, start_node)

print("=== (a) Shortest Path Tree (from A using Dijkstra) ===")
for node, dist in distances.items():
    print(f"Node {node}: shortest distance = {dist}, path = {' -> '.join(paths[node])}")
print()

MST = nx.minimum_spanning_tree(G, algorithm='prim')

print("=== (b) Minimum Spanning Tree (Prim’s Algorithm) ===")
total_weight = sum(data['weight'] for u, v, data in MST.edges(data=True))
for u, v, data in MST.edges(data=True):
    print(f"{u} - {v} : {data['weight']}")
print(f"Total weight of MST: {total_weight}\n")

# Manual layout (adjusted for spacing)
pos = {
    'A': (0, 3),
    'B': (1, 5),
    'C': (1.5, 3),
    'D': (1.8, 1.2),
    'E': (3.3, 4),
    'F': (3.4, 2),
    'G': (5, 3),
    'H': (6.2, 2),
    'I': (6.2, 4.3)
}

labels = nx.get_edge_attributes(G, 'weight')

plt.figure(figsize=(16, 6))

# Original Weighted Graph
plt.subplot(1, 3, 1)
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=900, font_weight='bold', font_size=10)
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8)
plt.title("Original Weighted Graph")

# Shortest Path Tree (SPT)
plt.subplot(1, 3, 2)
SPT_edges = []
for node, path in paths.items():
    if len(path) > 1:
        SPT_edges.append((path[-2], path[-1]))
nx.draw(G, pos, with_labels=True, node_color='lightgreen', node_size=900, font_weight='bold', font_size=10)
nx.draw_networkx_edges(G, pos, edgelist=SPT_edges, width=3, edge_color='green')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8)
plt.title("Shortest Path Tree (Dijkstra from A)")

# Minimum Spanning Tree (MST)
plt.subplot(1, 3, 3)
nx.draw(G, pos, with_labels=True, node_color='lightcoral', node_size=900, font_weight='bold', font_size=10)
nx.draw_networkx_edges(G, pos, edgelist=MST.edges(), width=3, edge_color='red')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8)
plt.title("Minimum Spanning Tree (Prim’s)")

plt.tight_layout()
plt.show()
