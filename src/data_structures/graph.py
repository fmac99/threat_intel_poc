import networkx as nx
import matplotlib.pyplot as plt
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class GraphProperties:
    directed: bool = False
    weighted: bool = False
    labeled: bool = True

class Graph:
    def __init__(self, properties: Optional[GraphProperties] = None):
        self.properties = properties or GraphProperties()
        self.graph = nx.DiGraph() if self.properties.directed else nx.Graph()
        
    def add_node(self, node_id: str, **attrs) -> None:
        """Add node with attributes"""
        self.graph.add_node(node_id, **attrs)
        
    def add_edge(self, source: str, target: str, **attrs) -> None:
        """Add edge with attributes"""
        if self.properties.weighted and 'weight' not in attrs:
            attrs['weight'] = 1.0
        self.graph.add_edge(source, target, **attrs)
        
    def remove_node(self, node_id: str) -> None:
        """Remove node and its edges"""
        self.graph.remove_node(node_id)
        
    def remove_edge(self, source: str, target: str) -> None:
        """Remove edge between nodes"""
        self.graph.remove_edge(source, target)
        
    def get_neighbors(self, node_id: str) -> List[str]:
        """Get list of neighboring nodes"""
        return list(self.graph.neighbors(node_id))
        
    def get_node_attributes(self, node_id: str) -> Dict:
        """Get all attributes of a node"""
        return dict(self.graph.nodes[node_id])
        
    def get_edge_attributes(self, source: str, target: str) -> Dict:
        """Get all attributes of an edge"""
        return dict(self.graph.edges[source, target])
        
    def to_dict(self) -> Dict:
        """Export graph to dictionary"""
        return nx.node_link_data(self.graph)
        
    def from_dict(self, data: Dict) -> None:
        """Import graph from dictionary"""
        self.graph = nx.node_link_graph(data)
        
    def save(self, filepath: str) -> None:
        """Save graph to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f)
            
    def load(self, filepath: str) -> None:
        """Load graph from JSON file"""
        with open(filepath, 'r') as f:
            self.from_dict(json.load(f))
            
    def visualize(self, figsize=(10,10)) -> None:
        """Visualize graph using NetworkX"""
        plt.figure(figsize=figsize)
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, 
                with_labels=self.properties.labeled,
                node_color='lightblue',
                edge_color='gray',
                font_size=8,
                node_size=500)
        plt.show()