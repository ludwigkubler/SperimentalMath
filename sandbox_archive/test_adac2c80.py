# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

# Helper functions for Gaussian elimination and matrix operations
def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rref = [row[:] for row in matrix]
    
    for i in range(rows):
        # Find pivot
        max_row = i
        for j in range(i+1, rows):
            if abs(rref[j][i]) > abs(rref[max_row][i]):
                max_row = j
        
        # Swap rows
        rref[i], rref[max_row] = rref[max_row], rref[i]
        
        # Eliminate below pivot
        for j in range(i+1, rows):
            factor = -rref[j][i] / rref[i][i]
            for k in range(cols):
                rref[j][k] += factor * rref[i][k]
    
    return rref

def rank(matrix):
    rref = gaussian_elimination(matrix)
    rank = 0
    for row in rref:
        if any(row):
            rank += 1
    return rank

# Function to generate a random k-clique graph
def generate_k_clique(n, k):
    G = [[0]*n for _ in range(n)]
    nodes = list(range(n))
    random.shuffle(nodes)
    clique_nodes = nodes[:k]
    for u in clique_nodes:
        for v in clique_nodes:
            if u < v:
                G[u][v] = G[v][u] = 1
    return G

# Function to compute tree-width (simplified version using BFS)
def tree_width(G):
    n = len(G)
    degree = [sum(row) for row in G]
    leaves = [i for i, d in enumerate(degree) if d == 1]
    
    while leaves:
        leaf = leaves.pop()
        for neighbor in range(n):
            if G[leaf][neighbor]:
                G[leaf][neighbor] = G[neighbor][leaf] = 0
                degree[neighbor] -= 1
                if degree[neighbor] == 1:
                    leaves.append(neighbor)
    
    return n - len(leaves)

# Main function to run a single trial
def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    k = random.randint(3, min(n-1, 6))
    G = generate_k_clique(n, k)
    
    config_space_rank = rank(G)
    tw = tree_width(G)
    
    if tw == 0:
        return {
            "metric_name": "rank/tw_ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "tree-width is zero, undefined for this conjecture"
        }
    
    ratio = Fraction(config_space_rank, tw)
    return {
        "metric_name": "rank/tw_ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": True if ratio <= 2 else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results]
    conjecture_holds = all(r["conjecture_holds"] for r in results)
    
    if conjecture_holds:
        mean = sum(metric_values) / len(metric_values)
        std_dev = math.sqrt(sum((x - mean)**2 for x in metric_values) / len(metric_values))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank/tw_ratio > 2\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")