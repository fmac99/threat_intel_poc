from data_structures.graph import Graph




def main():

    graph = Graph()
    for i in range(5):
        graph.add_node(f"Node {i}")

    graph.add_edge("Node 0", "Node 1")
    graph.add_edge("Node 0", "Node 2")
    graph.add_edge("Node 1", "Node 3")
    graph.add_edge("Node 2", "Node 4")


    graph.visualize()