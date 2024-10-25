import pandas as pd
import networkx as nx
from pyvis.network import Network
import os

# Load CSV files
group_data = pd.read_csv('data/01_group.csv', delimiter=';')
person_data = pd.read_csv('data/02_person.csv', delimiter=';')
project_data = pd.read_csv('data/03_project.csv', delimiter=';')

# Create network graph
G = nx.Graph()

# Add group nodes
for _, row in group_data.iterrows():
    G.add_node(row['id'], label=row['name'], type='group', title=f"Type: {row['type']}<br>Focus: {row['focus']}", url=row['url'])

# Add person nodes and edges to groups and projects
for _, row in person_data.iterrows():
    G.add_node(row['id'], label=row['name'], type='person', title=f"Employer: {row['employer']}", url=row['orcid'])
    
    # Link person to their employer group(s)
    if pd.notna(row['employer']):
        for employer in row['employer'].split('; '):
            G.add_edge(row['id'], employer)
    
    # Link person to projects
    if pd.notna(row['involved in']):
        for project in row['involved in'].split('; '):
            G.add_edge(row['id'], project)

# Add project nodes and edges to leading groups
for _, row in project_data.iterrows():
    G.add_node(row['id'], label=row['name'], type='project', title=f"Keywords: {row['keywords']}", url=row['url'])
    
    # Link project to lead group(s)
    if pd.notna(row['lead']):
        for lead in row['lead'].split('; '):
            G.add_edge(row['id'], lead)

# Create the network visualisation using Pyvis
net = Network(notebook=False, height='750px', width='100%', bgcolor='#ffffff', font_color='black', directed=False)
net.from_nx(G)

# Configure physics for better visualisation
net.set_options('''var options = {
  "nodes": {
    "shape": "dot",
    "scaling": {
      "min": 10,
      "max": 30
    }
  },
  "physics": {
    "barnesHut": {
      "gravitationalConstant": -20000,
      "springLength": 150
    }
  }
}''')

# Save the interactive visualisation as an HTML file
output_folder = 'docs'
os.makedirs(output_folder, exist_ok=True)
net.save_graph(os.path.join(output_folder, 'network.html'))

# Create a filterable table (aggregated CSV)
combined_data = pd.concat([group_data, person_data, project_data], axis=0, ignore_index=True)
combined_data.to_csv(os.path.join(output_folder, 'combined_data.csv'), index=False)

print("Network visualization saved as 'docs/network.html' and combined data saved as 'docs/combined_data.csv'.")
