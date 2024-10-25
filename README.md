# Digital Humanities Landscape Switzerland

Digital Humanities Landscape Switzerland (`dh-landscape-ch`) is intended to be an interactive, web-based overview of the Digital Humanities field in Switzerland. It will feature a network-style visualisation of projects, organisations, and researchers, allowing users to explore connections and filter information based on different criteria. The aim is to foster collaboration and provide insights into the Swiss Digital Humanities community.

**This is indeed a work in progress. Stay tuned.**

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
4. **Aggregating Data**: The script also generates a combined CSV (`combined_data.csv`) that contains all relevant information for filtering and further analysis.
5. **Saving Outputs**: The resulting network visualization is saved as `network.html` in the `docs` folder, which will be used for deployment via GitHub Pages. The combined CSV is also saved in the `docs` folder.

The interactive visualization will be accessible via `https://jraemysfa.github.io/dh-landscape-ch/network.html`.
