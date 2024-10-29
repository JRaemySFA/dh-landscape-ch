import pandas as pd
import networkx as nx
from pyvis.network import Network
import os
import math

# Load CSV files
group_data = pd.read_csv('data/01_group.csv', delimiter=';')
person_data = pd.read_csv('data/02_person.csv', delimiter=';')
project_data = pd.read_csv('data/03_project.csv', delimiter=';')

# Create network graph
G = nx.DiGraph()

# Add group nodes
for _, row in group_data.iterrows():
    G.add_node(row['id'], label=row['name'], type='group', title=f"<b>Type:</b> {row['type']}<br><b>Focus:</b> {row['focus']}<br><a href='{row['url']}' target='_blank'>Website</a>", color='lightblue')

# Add person nodes and edges to groups and projects
for _, row in person_data.iterrows():
    G.add_node(row['id'], label=row['name'], type='person', title=f"<b>Employer:</b> {row['employer']}<br><a href='{row['orcid']}' target='_blank'>ORCID</a>", color='lightgreen')
    
    # Link person to their employer group(s)
    if pd.notna(row['employer']):
        for employer in row['employer'].split('; '):
            G.add_edge(row['id'], employer, label='employed by', arrowhead='vee')
    
    # Link person to affiliated groups
    if pd.notna(row['affiliated in']):
        for affiliation in row['affiliated in'].split('; '):
            G.add_edge(row['id'], affiliation, label='affiliated with', arrowhead='vee')
    
    # Link person to projects
    if pd.notna(row['involved in']):
        for project in row['involved in'].split('; '):
            G.add_edge(row['id'], project, label='involved in', arrowhead='vee')

# Add project nodes and edges to leading groups
for _, row in project_data.iterrows():
    G.add_node(row['id'], label=row['name'], type='project', title=f"<b>Keywords:</b> {row['keywords']}<br><a href='{row['url']}' target='_blank'>Project Link</a>", color='lightcoral')
    
    # Link project to lead group(s)
    if pd.notna(row['lead']):
        for lead in row['lead'].split('; '):
            G.add_edge(row['id'], lead, label='led by', arrowhead='vee')

# Add edges between groups (parent or based in relationships)
for _, row in group_data.iterrows():
    if pd.notna(row['member of']):
        for parent in row['member of'].split('; '):
            G.add_edge(row['id'], parent, label='member of', arrowhead='vee')
    if pd.notna(row['parent']):
        G.add_edge(row['id'], row['parent'], label='based in', arrowhead='vee')

# Create the network visualisation using Pyvis
net = Network(notebook=False, height='750px', width='100%', bgcolor='#ffffff', font_color='black', directed=True)
net.from_nx(G)

# Set node size based on degree (logarithmic scaling)
for node in net.nodes:
    degree = G.degree(node['id'])
    node['size'] = math.log(degree + 1) * 10

# Configure physics for better visualisation and enable filtering
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
  },
  "interaction": {
    "hover": true,
    "navigationButtons": true,
    "multiselect": true
  },
  "edges": {
    "arrows": {
      "to": {
        "enabled": true
      }
    }
  },
  "manipulation": {
    "enabled": true
  },
  "filter": {
    "nodes": {
      "filterByType": {
        "type": ["group", "person", "project"]
      }
    }
  }
}''')

# Save the interactive visualisation as an HTML file
output_folder = 'docs'
os.makedirs(output_folder, exist_ok=True)
net.save_graph(os.path.join(output_folder, 'index.html'))

print("Network visualization saved as 'docs/index.html'.")