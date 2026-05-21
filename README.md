# Knowledge Graph Exploration: MetaFam Analysis

Welcome to the **Knowledge Graph Exploration** repository (originally the Precog Graph Task). This project explores the **MetaFam** dataset—a synthetic Knowledge Graph representing complex multi-generational family structures. The goal is to apply graph theory, community detection, rule mining, and link prediction techniques to analyze family dynamics and recover hidden relationships.

##  Directory Structure

```plaintext
precog_graph_task/
├── MetaFam_dataset/            # The raw dataset
│   ├── train.txt               # Main triples file (head, relation, tail)
│   └── test.txt                # Test set for link prediction
├── images/                     # Generated plots and visualizations
├── models/                     # Saved ML models (Node2Vec, RGCN embeddings)
├── notebooks/                  # Step-by-step analysis notebooks
│   ├── 01_dataset_exploration.ipynb
│   ├── 02_family_clusters.ipynb
│   ├── 03_rule_mining.ipynb
│   └── 04_link_prediction.ipynb
├── README.md                   # This file

```

---

##  How to Run

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Aakarsh1402/precog_graph_task.git
    cd precog_graph_task
    ```

2.  **Install Dependencies**
    Ensure you have Python installed, then run:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Notebooks**
    Launch Jupyter Lab or Notebook to explore the tasks interactively:
    ```bash
    jupyter notebook
    ```
    *Start with `01_dataset_exploration.ipynb` and proceed in order.*

---

##  Dependencies

The project relies on standard data science and graph analysis libraries:

*   **Core:** `pandas`, `numpy`, `scipy`
*   **Graph Analysis:** `networkx`
*   **Machine Learning:** `scikit-learn`
*   **Visualization:** `matplotlib`
*   **Environment:** `jupyter`

*(See `requirements.txt` for the full list)*

---

##  Project Approach & methodology

The project is divided into four sequential tasks, each building on the previous one. We combine traditional **graph theory** (centrality, paths) with modern **machine learning** (embeddings, GNNs).

### **Task 1: Dataset Exploration**
*   **Goal:** Understand the "Family" structure of the graph.
*   **Method:** Computed macro-statistics (degree distribution, diameter, density). We analyzed **Centrality metrics** (Betweenness, PageRank) to find "key" figures in families and visualized the largest families using force-directed layouts.
*   **Output:** Generated heatmaps and ego-graphs showing that middle-generation members (parents) are the structural backbone of families.

### **Task 2: Community Detection**
*   **Goal:** Blindly recover family clusters without using labels and find sub-communities (households).
*   **Method:**
    *   **Louvain/Leiden:** Perfect at recovering the 50 disconnected families.
    *   **Node2Vec + KMeans:** Learned structural embeddings that naturally separated families in vector space.
    *   **WRD (Weighted Relationship Distance):** A novel metric we designed to measure "relatedness" more accurately than simple hop count (e.g., distinguishing siblings vs. distant cousins).
*   **Output:** Comparison tables of Modularities and Heatmaps of the new WRD metric.

### **Task 3: Rule Mining**
*   **Goal:** Discover logical rules that govern family relationships (e.g., `Mother(A, B) ^ Father(B, C) => GrandMother(A, C)`).
*   **Method:** We used **AMIE**-style rule mining logic to find Horn clauses. We evaluated rules based on **Support** (frequency) and **Confidence** (reliability).
*   **Output:** A prioritized list of high-confidence rules that can infer missing links.

### **Task 4: Link Prediction**
*   **Goal:** Predict missing edges (e.g., infer `FatherOf` given other relations).
*   **Method:**
    *   **Heuristic:** Used Jaccard Coefficient and Adamic-Adar.
    *   **Embedding-Based:** Implemented **TransE** (Translational Embedding) and **Node2Vec**.
    *   **GNN:** Experimented with **R-GCN** (Relational Graph Convolutional Network) to capture complex multi-relational patterns.
*   **Output:** Metrics (MRR, Hits@10) comparing the performance of heuristic vs. deep learning approaches.

---

> *This repository was created as part of the Precog Graph Theory entrance task.*



