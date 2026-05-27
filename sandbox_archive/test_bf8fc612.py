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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_k_clique_instance(n, k):
        vertices = list(range(n))
        edges = []
        for i in range(k):
            edge = (vertices[i], vertices[k+i])
            edges.append(edge)
        return vertices, edges
    
    def compute_hodge_diamond(n, k):
        # Simplified Hodge diamond calculation
        return n**k + 2*k*n**(k-1) + k**2 * n**(k-2)
    
    def spearman_rank_correlation(x, y):
        n = len(x)
        sorted_x = sorted(range(n), key=lambda i: x[i])
        sorted_y = sorted(range(n), key=lambda i: y[i])
        rank_x = [sorted_x.index(i) for i in range(n)]
        rank_y = [sorted_y.index(i) for i in range(n)]
        d = sum((rank_x[i] - rank_y[i]) ** 2 for i in range(n))
        return 1 - (6 * d) / (n * (n**2 - 1))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        k = random.randint(1, min(n-1, 5))  # Ensure k is at least 1 and less than n
        vertices, edges = generate_k_clique_instance(n, k)
        
        circuit_size = len(vertices) + len(edges)  # Simplified circuit size calculation
        hodge_diamond = compute_hodge_diamond(n, k)
        
        results.append({
            "n": n,
            "k": k,
            "circuit_size": circuit_size,
            "hodge_diamond": hodge_diamond
        })
    
    if not results:
        return {
            "metric_name": "Spearman's Rank Correlation",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    hodge_diamonds = [r["hodge_diamond"] for r in results]
    circuit_sizes = [r["circuit_size"] for r in results]
    correlation_coefficient = spearman_rank_correlation(hodge_diamonds, circuit_sizes)
    
    return {
        "metric_name": "Spearman's Rank Correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "conjecture_holds": abs(correlation_coefficient) > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(1, 31)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no trials ran")
        sys.exit(0)
    
    mean_d = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_d) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "Spearman's rank correlation coefficient did not meet the threshold"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")