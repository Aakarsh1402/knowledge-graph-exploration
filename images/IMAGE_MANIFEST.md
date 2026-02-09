# Image Manifest — mapping images to tasks

Images are organized into task-specific subfolders. Each notebook saves to its corresponding subfolder.

## Task 1 — Dataset Exploration (`images/task1/`)
| File | Description |
|------|-------------|
| `relation_distribution.png` | Bar chart of 28 relation types coloured by generational category |
| `degree_distribution.png` | 3-panel histogram (in-degree, out-degree, total) |
| `family_sizes.png` | Connected component size distribution |
| `metrics_dashboard.png` | Summary dashboard: density, clustering, diameter |
| `centrality_heatmap.png` | Heatmap of top nodes across 4 centrality measures |
| `generation_depth.png` | Generation depth per family |
| `family_clusters.png` | Spring-layout plots of 4 sample families |
| `generation_ladder.png` | Layered generation view of the largest family |
| `bridge_node.png` | Ego graph of the highest-betweenness node |
| `pagerank_ego.png` | Ego graph of the highest-PageRank node |
| `clustering_distribution.png` | Distribution of local clustering coefficients |

## Task 2 — Community & Subfamily Analysis (`images/task2/`)
| File | Description |
|------|-------------|
| `louvain_resolution_sweep.png` | Modularity vs resolution for Louvain |
| `leiden_vs_louvain_sweep.png` | Leiden vs Louvain comparison sweep |
| `girvan_newman_modularity.png` | Girvan-Newman modularity curve |
| `girvan_newman_splits.png` | Community splits at optimal cut |
| `node2vec_pca.png` | PCA of node2vec embeddings |
| `node2vec_subfamily_elbow.png` | Elbow plot for subfamily clustering |
| `community_comparison.png` | Side-by-side comparison of methods |
| `subfamily_analysis.png` | Subfamily structure within families |
| `wkd_heatmap.png` | Wasserstein distance heatmap |
| `wkd_ward_vs_leiden.png` | Ward vs Leiden clustering comparison |
| `cross_family_wkd_profiles.png` | Cross-family distance profiles |

## Task 3 — Rule Mining (`images/task3/`)
| File | Description |
|------|-------------|
| `rule_mining_overview.png` | Confidence distribution of discovered rules |
| `relationship_inference.png` | Semantic inference examples |

## Notes
- Notebooks save images using relative paths: `../images/task{N}/<name>.png`
- Some images may be referenced in concept guides or the README as well.

