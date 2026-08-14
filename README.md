# Knowledge Graph Exploration: MetaFam Analysis

Welcome to the **Knowledge Graph Exploration** repository (originally the Precog Graph Task). This project explores the **MetaFam** dataset—a synthetic Knowledge Graph representing complex multi-generational family structures. The goal is to apply graph theory, community detection, rule mining, and link prediction techniques to analyze family dynamics and recover hidden relationships.

##  Directory Structure

```plaintext
knowledge-graph-exploration/
├── MetaFam_dataset/            # The raw dataset
│   ├── train.txt               # Main triples file (head, relation, tail)
│   └── test.txt                # Test set for link prediction
├── src/
│   └── metafam.py               # Shared constants (GEN_WEIGHTS, CLOSENESS_WEIGHTS) and
│                                 # helpers (data loading, generation assignment, broker
│                                 # scores, ...) used by all four notebooks
├── images/                     # Generated plots and visualizations (task1/–task4/)
├── models/                     # Saved ML models: Node2Vec embedding caches (.npy,
│                                 # regenerated automatically if deleted) and trained
│                                 # R-GCN / TransE checkpoints (.pt)
├── notebooks/                  # Step-by-step analysis notebooks
│   ├── 01_dataset_exploration.ipynb
│   ├── 02_family_clusters.ipynb
│   ├── 03_rule_mining.ipynb
│   └── 04_link_prediction.ipynb
├── report/
│   └── report.tex              # LaTeX source for report.pdf (compile with pdflatex)
├── report.pdf                  # Full write-up, all four tasks
├── requirements.txt
└── README.md                   # This file
```

---

##  How to Run

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Aakarsh1402/knowledge-graph-exploration.git
    cd knowledge-graph-exploration
    ```

2.  **Create a virtual environment and install dependencies**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate        # Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    pip install jupyter              # notebook runtime itself isn't in requirements.txt
    ```

3.  **Run the Notebooks, in order**
    ```bash
    jupyter notebook
    ```
    Run `01_dataset_exploration.ipynb` → `02_family_clusters.ipynb` →
    `03_rule_mining.ipynb` → `04_link_prediction.ipynb`, each "Restart & Run All".
    Notebook 02 depends on nothing from 01 at the code level, but the tasks build on
    each other narratively, so running in order is the intended path. Total runtime is
    roughly 15–25 minutes on a modern laptop CPU, dominated by Node2Vec (02) and R-GCN
    / TransE training (04); no GPU is required.

    `models/*.npy` are cached Node2Vec embeddings — delete them to force a retrain, or
    leave them to skip straight to the cached result. `models/*.pt` are the trained
    R-GCN and TransE checkpoints saved by notebook 04.

---

##  Dependencies

The project relies on standard data science, graph analysis, and deep learning libraries — see `requirements.txt` for the full pinned list:

*   **Core:** `numpy`, `pandas`, `scipy`
*   **Graph:** `networkx`, `python-louvain`, `leidenalg`, `python-igraph`, `node2vec`
*   **ML:** `scikit-learn`
*   **Deep learning:** `torch`, `torch-geometric`
*   **Visualization:** `matplotlib`
*   **Other:** `tqdm`, `jupyter` (for running the notebooks; not pinned in requirements.txt)

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
    *   **GNN:** **R-GCN** (Relational Graph Convolutional Network) + DistMult decoder, to capture multi-relational graph structure.
    *   **Embedding-Based:** **TransE** (Translational Embedding), both with random negative sampling and with family-aware negative sampling (using the family structure from Task 1/2 to generate harder negatives).
*   **Output:** Metrics (MRR, Hits@1/3/10) comparing R-GCN against both TransE variants.

---

##  Known limitations

- **Task 4's test set covers only 4 of 28 relations** (`sonOf`, `daughterOf`, `motherOf`, `fatherOf` — immediate parent/child links only). Models train on all 28 relations, but every reported test metric — including the per-relation breakdown — is scored on those four relations only. See notebook 04 §1 for the measured breakdown and §9/"Key Findings" for the fuller caveat.
- **The `CLOSENESS_WEIGHTS` used in Task 2's WRD metric are hand-set**, not learned or independently validated — they operationalize a real framework from the family-sociology literature (intergenerational solidarity; see notebook 02 §1 for citations), but the specific 1–10 scores are a modelling choice, not a measurement.
- **`src/metafam.py`** holds the constants (`GEN_WEIGHTS`, `CLOSENESS_WEIGHTS`) and helpers (`load_triples`, `build_digraph`, `assign_generations`, `compute_broker_scores`, ...) shared by all four notebooks — it's the single source of truth if you want to check or change how generation levels or closeness weights are defined, rather than a specific notebook cell.
- **Committed notebook outputs:** the notebooks in this repo are committed *with* their cell outputs (plots, printed tables) rather than cleared — this is a deliberate choice so the analysis renders directly on GitHub without needing to run anything, at the cost of larger diffs on every re-run.

---

> *This repository was created as part of the Precog Graph Theory entrance task.*
