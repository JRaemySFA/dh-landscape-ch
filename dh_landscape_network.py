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
    title = f"<b>{row['name']}</b><br><b>Type:</b> {row['type']}<br><b>Focus:</b> {row['focus']}"
    if pd.notna(row['url']):
        title += f"<br><a href='{row['url']}' target='_blank'>Website</a>"
    G.add_node(row['id'], label=row['name'], type='group', title=title, color='lightblue')

# Add person nodes and edges to groups and projects
for _, row in person_data.iterrows():
    # Get employer names
    employer_names = []
    if pd.notna(row['employer']):
        for employer_id in row['employer'].split('; '):
            employer_row = group_data[group_data['id'] == employer_id]
            if not employer_row.empty:
                employer_names.append(employer_row.iloc[0]['name'])
    employer_str = '; '.join(employer_names)
    
    # Get affiliations
    affiliation_names = []
    if pd.notna(row['affiliated in']):
        for affiliation_id in row['affiliated in'].split('; '):
            affiliation_row = group_data[group_data['id'] == affiliation_id]
            if not affiliation_row.empty:
                affiliation_names.append(affiliation_row.iloc[0]['name'])
    affiliation_str = '; '.join(affiliation_names)

    # Get involved projects
    project_names = []
    if pd.notna(row['involved in']):
        for project_id in row['involved in'].split('; '):
            project_row = project_data[project_data['id'] == project_id]
            if not project_row.empty:
                project_names.append(project_row.iloc[0]['name'])
    project_str = '; '.join(project_names)

    # Create title for person node
    title = f"<b>{row['name']}</b><br><b>Employer:</b> {employer_str}"
    if affiliation_str:
        title += f"<br><b>Affiliations:</b> {affiliation_str}"
    if project_str:
        title += f"<br><b>Projects Involved:</b> {project_str}"
    if pd.notna(row['orcid']):
        title += f"<br><a href='{row['orcid']}' target='_blank'>ORCID</a>"
    G.add_node(row['id'], label=row['name'], type='person', title=title, color='lightgreen')
    
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
    title = f"<b>{row['name']}</b><br><b>Keywords:</b> {row['keywords']}"
    if pd.notna(row['start']) and pd.notna(row['end']):
        start_year = int(row['start'])
        end_year = int(row['end'])
        title += f"<br><b>Timeline:</b> {start_year} - {end_year}"
    if pd.notna(row['url']):
        title += f"<br><a href='{row['url']}' target='_blank'>Project Link</a>"
    G.add_node(row['id'], label=row['name'], type='project', title=title, color='lightcoral')
    
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
        for parent in row['parent'].split('; '):
            G.add_edge(row['id'], parent, label='parent', arrowhead='vee')
    if pd.notna(row['based in']):
        for location in row['based in'].split('; '):
            G.add_edge(row['id'], location, label='based in', arrowhead='vee')

# Create the network visualisation using Pyvis
net = Network(notebook=False, height='100vh', width='100vw', bgcolor='#ffffff', font_color='black', directed=True)
net.from_nx(G)

# Set node size based on degree (logarithmic scaling with increased factor), excluding affiliation links for people
for node in net.nodes:
    node_id = node['id']
    if node['type'] == 'person':
        # Count only non-affiliation links for people
        degree = sum(1 for _, _, d in G.out_edges(node_id, data=True) if d['label'] != 'affiliated with') + G.in_degree(node_id)
    else:
        degree = G.degree(node_id)
    node['size'] = math.log(degree + 1) * 30  # Increased scaling factor for better visualization


# Configure physics for better visualisation
net.set_options('''var options = {
  "nodes": {
    "shape": "dot",
    "scaling": {
      "min": 20,
      "max": 50
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
  }
}''')

# Add H1 title and schema.org metadata to the HTML
html_header = '''
<!DOCTYPE html>
<html>
<head>
    <title>Digital Humanities Landscape Switzerland (October 2024)</title>
    <style>
        body, html {
            height: 100vh;
            width: 100vw;
            margin: 0;
            padding: 0;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
        }
        #network {
            flex-grow: 1;
            width: 100%;
            height: 100%;
        }
        #search-container {
            position: absolute;
            top: 10px;
            right: 20px;
            z-index: 1000;
        }
        #searchInput {
            padding: 5px;
            font-size: 16px;
        }
        #searchResults {
            background-color: white;
            border: 1px solid #ccc;
            max-height: 200px;
            overflow-y: auto;
            position: absolute;
            top: 40px;
            right: 20px;
            width: 200px;
            z-index: 1001;
        }
        .search-result {
            padding: 5px;
            cursor: pointer;
        }
        .search-result:hover {
            background-color: #f0f0f0;
        }
    </style>
    <script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "WebSite",
        "name": "Digital Humanities Landscape Switzerland",
        "author": {
            "@type": "Person",
            "givenName": "Julien Antoine",
            "familyName": "Raemy",
            "gender": "Male",
            "url": "https://julsraemy.ch",
            "affiliation": [
                {
                    "@type": "ArchiveOrganization",
                    "name": "Swiss Federal Archives",
                    "location": "Bern, Switzerland",
                    "url": "https://www.bar.admin.ch/",
                    "sameAs": "https://ror.org/00t6xza10"
                }
            ],
            "sameAs": [
                "https://orcid.org/0000-0002-4711-5759", 
                "https://phd.julsraemy.ch", 
                "https://hcommons.social/@julsraemy",
                "https://scholar.google.ch/citations?user=pGROUG0AAAAJ",
                "https://www.linkedin.com/in/julienaraemy/"
            ]
        },
        "datePublished": "Tue Oct 29 2024 00:00:00 GMT+0000 (Coordinated Universal Time)",
        "description": "An interactive overview of the Digital Humanities field in Switzerland, showcasing connections between projects, organisations, and researchers.",
        "keywords": "Digital Humanities, Switzerland, Network Visualization, Julien A. Raemy"
    }
    </script>
    <script type="text/javascript">
        function searchNodes() {
            var searchTerm = document.getElementById('searchInput').value.toLowerCase();
            var allNodes = network.body.data.nodes.get();
            var searchResults = document.getElementById('searchResults');
            searchResults.innerHTML = '';

            allNodes.forEach(function(node) {
                if (node.label.toLowerCase().includes(searchTerm) || (node.title && node.title.toLowerCase().includes(searchTerm))) {
                    var resultItem = document.createElement('div');
                    resultItem.className = 'search-result';
                    resultItem.innerText = node.label;
                    resultItem.onclick = function() {
                        network.focus(node.id, {
                            scale: 1.5,
                            animation: {
                                duration: 1000,
                                easingFunction: 'easeInOutQuad'
                            }
                        });
                    };
                    searchResults.appendChild(resultItem);
                }
            });
        }
    </script>
</head>
<body>
    <h1>Digital Humanities Landscape Switzerland (October 2024)</h1>
    <div id="search-container">
        <input type="text" id="searchInput" placeholder="Search for a node..." onkeyup="searchNodes()">
        <div id="searchResults"></div>
    </div>
    <div id="network"></div>
    <p style="font-size: small;">Julien A. Raemy, 2024. <a href="https://github.com/JRaemySFA/dh-landscape-ch" target="_blank">GitHub Repository</a></p>
</body>
</html>
'''

# Generate HTML
output_path = 'docs/index.html'
net.save_graph(output_path)
with open(output_path, 'r') as f:
    content = f.read()

with open(output_path, 'w') as f:
    f.write(html_header + content)

print(f"Network visualisation has been created and saved as '{output_path}'")
