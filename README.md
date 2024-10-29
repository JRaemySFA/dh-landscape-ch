# Digital Humanities Landscape Switzerland

Digital Humanities Landscape Switzerland (`dh-landscape-ch`) is intended to be an interactive, web-based overview of the Digital Humanities field in Switzerland. It features a network-style visualisation of projects, organisations, and researchers, allowing users to explore connections and filter information based on different criteria. The aim is to foster collaboration and provide insights into the Swiss Digital Humanities community.

This overview is a snapshot of (a surely not complete) DH Landscape in Switzerland as of October 2024. The focus has mainly been on institutes and laboratories that market themselves as being part of Digital Humanities, but DH is a big tent, and surely many people are missing.

## How It Works

### CSV Files
The project relies on three CSV files to create the network:
- **01_group.csv**: Contains information about organisations and institutions involved in Digital Humanities in Switzerland. Each row represents a group, such as an academic lab, consortium, or research infrastructure.
- **02_person.csv**: Contains details of researchers and collaborators in the Digital Humanities field. Each row represents a person and includes their affiliations and projects they are involved in.
- **03_project.csv**: Contains information about research projects in the Digital Humanities. Each row represents a project, including keywords, start and end dates, and leading organisations.

### Script Overview
The Python script (`dh_landscape_network.py`) processes these CSV files to create an interactive network visualization:
1. **Loading Data**: The script loads the three CSV files using `pandas`, which allows for efficient data handling.
2. **Creating the Network**: The script uses `networkx` to create a network graph, where nodes represent groups, people, and projects. Edges are added to represent relationships between these entities (e.g., a researcher involved in a project, or a group leading a project).
3. **Visualizing the Network**: The script uses `pyvis` to convert the `networkx` graph into an interactive HTML visualization. This allows users to explore the network dynamically.
4. **Saving Outputs**: The resulting network visualization is saved as `index.html` in the `docs` folder, which is used for deployment via GitHub Pages.

The interactive visualization is accessible via [https://jraemysfa.github.io/dh-landscape-ch/](https://jraemysfa.github.io/dh-landscape-ch/).

## Node Size Explanation
The size of each node in the network graph is proportional to the number of connections (inbound and outbound edges) associated with it. The size calculation uses a logarithmic scale to ensure that nodes with many connections do not overwhelm the visualization. For **person nodes**, only non-affiliation connections (e.g., projects or employers) are considered to determine the size. This helps to highlight key contributors, institutions, and projects in the Digital Humanities landscape.

## Note on Organisations
For organisations as employers, DH-related labs or institutes have been used as employers when they existed. If not, the name of the parent organisation (e.g., university) has been used. Labs and departments are linked to their parent organisations in the network.

## Contributing
Pull requests and issues are welcome to help make the network more complete or to correct any mistakes. Please feel free to contribute.

## Cite this repository


[![DOI](https://zenodo.org/badge/873575817.svg)](https://doi.org/10.5281/zenodo.14006033)

