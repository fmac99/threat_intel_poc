import streamlit as st
import networkx as nx
import random
import plotly.graph_objects as go
import pandas as pd


def create_asset_graph():
    # Change to DiGraph for directed edges
    G = nx.DiGraph()
    
    # Define assets
    servers = [f"Server{i}" for i in range(1, 7)]  # 6 servers
    printer = ["Printer1"]                        # 1 printer
    devices = [f"Switch{i}" for i in range(1, 4)]  # 3 networking devices
    threats = [f"Threat{i}" for i in range(1, 4)]  # 3 threats
    
    # Add asset nodes
    for s in servers:
        G.add_node(s, asset_type="server")
    for p in printer:
        G.add_node(p, asset_type="printer")
    for d in devices:
        G.add_node(d, asset_type="network_device")
    
    # Add threat nodes
    for t in threats:
        G.add_node(t, asset_type="threat")
    
    # Randomly connect each device to some servers
    # Using device -> server for demonstration
    for d in devices:
        connect_count = random.randint(1, len(servers))
        connected_servers = random.sample(servers, k=connect_count)
        for s in connected_servers:
            G.add_edge(d, s, name="connects")
    
    # Randomly connect threats to assets as directed edges (threat -> asset)
    all_assets = servers + printer + devices
    for t in threats:
        threatened_assets_count = random.randint(1, len(all_assets))
        targeted_assets = random.sample(all_assets, k=threatened_assets_count)
        for asset in targeted_assets:
            risk_score = round(random.uniform(1.0, 10.0), 2)
            G.add_edge(t, asset, name="threatens", risk_score=risk_score)
    
    return G

def display_asset_graph(G):
    # Generate layout positions
    pos = nx.spring_layout(G, seed=42)

    # Edge coordinates
    edge_x = []
    edge_y = []
    edge_text = []
    for source, target, data in G.edges(data=True):
        x0, y0 = pos[source]
        x1, y1 = pos[target]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        
        risk = data.get("risk_score", "")
        label = data.get("name", "")
        if risk != "":
            edge_text.append(f"{label} | Risk: {risk}")
        else:
            edge_text.append(label)
        edge_text.extend(["", ""])  # Align with None spacing

    edge_trace = go.Scatter(
        x=edge_x, 
        y=edge_y,
        line=dict(width=1, color='gray'),
        hoverinfo='none',
        mode='lines'
    )

    # Node coordinates and colors
    node_x = []
    node_y = []
    node_text = []
    node_colors = []
    for node, ndata in G.nodes(data=True):
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(str(node))
        
        # Color by asset type
        if ndata.get('asset_type') == "server":
            node_colors.append("lightblue")
        elif ndata.get('asset_type') == "printer":
            node_colors.append("lightgreen")
        elif ndata.get('asset_type') == "network_device":
            node_colors.append("orange")
        else:  # threat
            node_colors.append("red")

    node_trace = go.Scatter(
        x=node_x, 
        y=node_y,
        mode='markers+text',
        text=node_text,
        textposition='top center',
        marker=dict(
            size=15,
            color=node_colors,
            line=dict(width=1, color='black')
        ),
        hoverinfo='text'
    )

    # Edge label placement (calculate midpoints)
    mid_x = []
    mid_y = []
    for i in range(0, len(edge_x), 3):
        if i + 1 < len(edge_x):
            x_mid = (edge_x[i] + edge_x[i+1]) / 2 if edge_x[i+1] is not None else edge_x[i]
            y_mid = (edge_y[i] + edge_y[i+1]) / 2 if edge_y[i+1] is not None else edge_y[i]
            mid_x.append(x_mid)
            mid_y.append(y_mid)

    edge_label_trace = go.Scatter(
        x=mid_x,
        y=mid_y,
        text=edge_text,
        mode='text',
        textposition='top center',
        hoverinfo='none'
    )

    fig = go.Figure(data=[edge_trace, node_trace, edge_label_trace],
                    layout=go.Layout(
                        title='Directed Threat & Asset Graph',
                        showlegend=False,
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        margin=dict(b=20, l=5, r=5, t=40)
                    ))
    
    st.plotly_chart(fig, use_container_width=True)

def display_graph_tables(G):
    # Prepare separate tabular data for nodes and edges
    node_data = []
    edge_data = []
    
    # Gather node data
    for node, attrs in G.nodes(data=True):
        node_type = attrs.get("asset_type", "unknown")
        for key, val in attrs.items():
            node_data.append({
                "Node Name": node,
                "Node Type": node_type,
                "Property_Name": key,
                "Property_Value": val
            })
    
    # Gather edge data
    for u, v, attrs in G.edges(data=True):
        edge_name = f"{u} -> {v}"
        edge_type = attrs.get("name", "unknown")
        for key, val in attrs.items():
            edge_data.append({
                "Edge Name": edge_name,
                "Edge Type": edge_type,
                "Property_Name": key,
                "Property_Value": val
            })

    # Convert to DataFrame
    node_df = pd.DataFrame(node_data, columns=["Node Name", "Node Type", "Property_Name", "Property_Value"])
    edge_df = pd.DataFrame(edge_data, columns=["Edge Name", "Edge Type", "Property_Name", "Property_Value"])
    
    # Display
    st.subheader("Nodes Table")
    st.data_editor(node_df, use_container_width=True, hide_index=True)
    
    st.subheader("Edges Table")
    st.data_editor(edge_df, use_container_width=True, hide_index=True)


def main():
    st.title("Directed Threat & Asset Graph")
    if st.button("Create & Display Graph"):
        graph = create_asset_graph()
        display_asset_graph(graph)
        display_graph_tables(graph)

if __name__ == "__main__":
    main()
