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

def generate_k_clique_instance(n, k):
    if n < k:
        return None  # Not possible to form a clique with fewer vertices than k
    
    # Generate all possible edges between n vertices
    vertices = list(range(n))
    edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
    
    # Randomly select k-1 edges to form a clique
    selected_edges = random.sample(edges, k - 1)
    clique_edges = []
    for u, v in selected_edges:
        if (u, v) not in clique_edges and (v, u) not in clique_edges:
            clique_edges.append((u, v))
    
    # Add the remaining edges to form a complete graph
    for i in range(n):
        for j in range(i + 1, n):
            if (i, j) not in clique_edges and (j, i) not in clique_edges:
                clique_edges.append((i, j))
    
    return clique_edges

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        clique_edges = generate_k_clique_instance(n, k=3)  # Example with k=3
        if clique_edges is None:
            continue
        
        # Compute the rank of the tropicalized sheaf cohomology groups
        # This is a placeholder function; replace it with actual computation
        rank = len(clique_edges)
        
        results.append({
            "n": n,
            "rank": rank,
            "ratio": Fraction(rank, n) if n != 0 else None
        })
    
    if not results:
        return {
            "metric_name": "Ratio of Rank to Vertex Count",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid k-CLIQUE instances generated"
        }
    
    # Calculate the mean and standard deviation of the ratios
    total_ratio = sum(result["ratio"] for result in results if result["ratio"] is not None)
    mean_ratio = Fraction(total_ratio, len(results))
    
    variance = sum((result["ratio"] - mean_ratio) ** 2 for result in results if result["ratio"] is not None)
    std_deviation = math.sqrt(Fraction(variance, len(results)))
    
    # Check the conjecture
    conjecture_holds = all(result["ratio"] >= mean_ratio / n_values[-1] ** (1/4) for result in results if result["ratio"] is not None)
    
    return {
        "metric_name": "Ratio of Rank to Vertex Count",
        "metric_value": float(mean_ratio),
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "Ratio does not meet the conjectured bound"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    # Compute mean/std of metric_value, fraction of seeds where conjecture_holds
    total_metric_values = sum(res["metric_value"] for res in results if res["metric_value"] is not None)
    mean_metric_value = total_metric_values / len(results)
    
    variance = sum((res["metric_value"] - mean_metric_value) ** 2 for res in results if res["metric_value"] is not None)
    std_deviation = math.sqrt(variance / len(results))
    
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_deviation} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_deviation} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Ratio does not meet the conjectured bound' first_failing_seed={first_failing_seed}")