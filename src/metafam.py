"""Shared constants and helpers for the MetaFam notebooks (01-04).

Centralises logic that used to be duplicated (and, in the case of
GEN_WEIGHTS and assign_generations, inconsistently duplicated) across the
four notebooks. See IMPROVEMENT_PLAN.md Phase 4.1.

Usage from a notebook in notebooks/:
    import sys; sys.path.insert(0, '..')
    from src.metafam import *
"""
from collections import deque
from pathlib import Path

import networkx as nx
import pandas as pd

__all__ = [
    "DATA_DIR",
    "GEN_WEIGHTS",
    "CLOSENESS_WEIGHTS",
    "PLOT_RCPARAMS",
    "PLOT_RCPARAMS_MINIMAL",
    "set_plot_style",
    "set_plot_style_minimal",
    "load_triples",
    "build_digraph",
    "families",
    "family_labels",
    "assign_generations",
    "validate_generations",
    "compute_broker_scores",
]

DATA_DIR = Path(__file__).resolve().parent.parent / "MetaFam_dataset"

# Generational offset carried by each relation: head is `weight` generations
# above tail (motherOf -> +1, sonOf -> -1, sisterOf -> 0, ...).
#
# firstCousinOnceRemoved is -1 (one generation apart), not 0: notebook 03
# establishes empirically (100% confidence, 55/55 support) that the relation
# means "my parent's cousin" (see 03 section 3.1) — a one-generation gap.
GEN_WEIGHTS = {
    # Parent / Child  (+-1 generation)
    'motherOf': 1, 'fatherOf': 1,
    'daughterOf': -1, 'sonOf': -1,
    # Grandparent / Grandchild  (+-2)
    'grandmotherOf': 2, 'grandfatherOf': 2,
    'granddaughterOf': -2, 'grandsonOf': -2,
    # Great-Grandparent / Great-Grandchild  (+-3)
    'greatGrandmotherOf': 3, 'greatGrandfatherOf': 3,
    'greatGranddaughterOf': -3, 'greatGrandsonOf': -3,
    # Siblings  (0)
    'sisterOf': 0, 'brotherOf': 0,
    # Aunt/Uncle & Niece/Nephew  (+-1)
    'auntOf': 1, 'uncleOf': 1,
    'nieceOf': -1, 'nephewOf': -1,
    # Great Aunt/Uncle  (+-2)
    'greatAuntOf': 2, 'greatUncleOf': 2,
    # Second Aunt/Uncle  (+-1, parent's cousin generation)
    'secondAuntOf': 1, 'secondUncleOf': 1,
    # Cousins  (0 - same generation)
    'girlCousinOf': 0, 'boyCousinOf': 0,
    # First-cousin-once-removed  (+-1 - one generation apart)
    'boyFirstCousinOnceRemovedOf': -1, 'girlFirstCousinOnceRemovedOf': -1,
    # Second cousins  (0 - same generation)
    'boySecondCousinOf': 0, 'girlSecondCousinOf': 0,
}

# Subjective emotional-closeness score (1=distant, 10=very close), operationalising
# "affectual solidarity" from Bengtson & Roberts (1991) / Dykstra & Fokkema (2011).
# See notebook 02 section 1 for the full rationale.
CLOSENESS_WEIGHTS = {
    'sisterOf': 9, 'brotherOf': 9,
    'motherOf': 10, 'fatherOf': 10, 'daughterOf': 10, 'sonOf': 10,
    'grandmotherOf': 7, 'grandfatherOf': 7, 'grandsonOf': 7, 'granddaughterOf': 7,
    'greatGrandmotherOf': 4, 'greatGrandfatherOf': 4,
    'greatGrandsonOf': 4, 'greatGranddaughterOf': 4,
    'auntOf': 6, 'uncleOf': 6, 'nieceOf': 6, 'nephewOf': 6,
    'greatAuntOf': 4, 'greatUncleOf': 4,
    'secondAuntOf': 3, 'secondUncleOf': 3,
    'girlCousinOf': 5, 'boyCousinOf': 5,
    'boyFirstCousinOnceRemovedOf': 3, 'girlFirstCousinOnceRemovedOf': 3,
    'boySecondCousinOf': 2, 'girlSecondCousinOf': 2,
}

# "Full" style, used by notebooks with hand-tuned axes (01, 04).
PLOT_RCPARAMS = {
    'figure.dpi': 130,
    'font.size': 10,
    'axes.titlesize': 12,
    'axes.titleweight': 'bold',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'figure.facecolor': 'white',
}

# Minimal style used by notebooks that only tweak dpi/font (02, 03).
PLOT_RCPARAMS_MINIMAL = {
    'figure.dpi': 120,
    'font.size': 10,
}


def set_plot_style():
    """Apply the shared 'full' MetaFam matplotlib style (notebooks 01, 04)."""
    import matplotlib.pyplot as plt
    plt.rcParams.update(PLOT_RCPARAMS)


def set_plot_style_minimal():
    """Apply the shared 'minimal' MetaFam matplotlib style (notebooks 02, 03)."""
    import matplotlib.pyplot as plt
    plt.rcParams.update(PLOT_RCPARAMS_MINIMAL)


def load_triples(path):
    """Load a MetaFam triples file into a DataFrame with columns head/relation/tail."""
    return pd.read_csv(path, sep=' ', header=None, names=['head', 'relation', 'tail'])


def build_digraph(df):
    """Build a directed graph from a triples DataFrame.

    nx.from_pandas_edgelist silently collapses parallel edges between the same
    (head, tail) pair, keeping only the last relation. We assert that doesn't
    happen instead of relying on it staying true.
    """
    dup_counts = df.groupby(['head', 'tail'])['relation'].nunique()
    n_collisions = int((dup_counts > 1).sum())
    assert n_collisions == 0, (
        f"{n_collisions} (head, tail) pairs carry more than one relation - "
        "build_digraph would silently drop one of them"
    )
    return nx.from_pandas_edgelist(df, 'head', 'tail', edge_attr='relation',
                                    create_using=nx.DiGraph())


def families(G):
    """Weakly connected components of a directed family graph."""
    return list(nx.weakly_connected_components(G))


def family_labels(components):
    """Map node -> family index (0-based) from a list of components."""
    return {n: i for i, comp in enumerate(components) for n in comp}


def assign_generations(G, comp, gen_weights):
    """BFS-assign a relative generation level to every node in `comp`.

    Root is min(comp) (deterministic - not set iteration order). For edge
    (u, rel, v): gens[v] = gens[u] - gen_weights[rel] (successor) or
    gens[u] + gen_weights[rel] (predecessor). Returns {node: generation};
    generation 0 is the root, not necessarily the oldest member.
    """
    sub = G.subgraph(comp)
    start = min(comp)
    gens = {start: 0}
    queue = deque([start])
    visited = {start}
    while queue:
        u = queue.popleft()
        for v in sub.successors(u):
            if v not in visited:
                rel = sub.get_edge_data(u, v).get('relation', '')
                gens[v] = gens[u] - gen_weights.get(rel, 0)
                visited.add(v)
                queue.append(v)
        for v in sub.predecessors(u):
            if v not in visited:
                rel = sub.get_edge_data(v, u).get('relation', '')
                gens[v] = gens[u] + gen_weights.get(rel, 0)
                visited.add(v)
                queue.append(v)
    return gens


def validate_generations(G, components, gen_weights):
    """Assign generations to every component and check internal consistency.

    For every directed edge (u, rel, v) inside a component, checks whether
    gens[v] == gens[u] - gen_weights[rel] (the invariant assign_generations'
    BFS enforces only along the tree it walks, never for the edges it
    doesn't traverse). See IMPROVEMENT_PLAN.md 1.4.

    Returns (all_gens, n_edges_checked, n_violations).
    """
    all_gens = {}
    n_edges = 0
    n_violations = 0
    for comp in components:
        gens = assign_generations(G, comp, gen_weights)
        all_gens.update(gens)
        sub = G.subgraph(comp)
        for u, v, d in sub.edges(data=True):
            rel = d.get('relation', '')
            n_edges += 1
            if gens[v] != gens[u] - gen_weights.get(rel, 0):
                n_violations += 1
    return all_gens, n_edges, n_violations


def compute_broker_scores(graph):
    """Broker score: degree x (1 - clustering) for nodes with degree > 1."""
    clust = nx.clustering(graph)
    deg = dict(graph.degree())
    return {n: deg[n] * (1 - clust[n]) for n in graph.nodes() if deg[n] > 1}
