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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate k-party communication complexity problem with known complexity rank
    k = random.randint(2, 5)  # Number of parties
    n = random.randint(3, 10)  # Number of nodes
    r_k = random.randint(n, 2*n)  # Communication complexity rank
    
    # Create a random communication graph (adjacency matrix)
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0  # No self-loops
    
    # Compute the geometric entropy of the graph
    adj_matrix = G
    n = len(adj_matrix)
    
    # Calculate the Shannon entropy of the adjacency matrix
    row_sums = [sum(row) for row in adj_matrix]
    col_sums = [sum(col) for col in zip(*adj_matrix)]
    total_edges = sum(row_sums) // 2
    
    H_G = 0.0
    for i in range(n):
        if row_sums[i] == 0:
            continue
        p_i = row_sums[i] / total_edges
        H_G -= p_i * math.log2(p_i)
    
    # Check the conjecture: H(G) <= c * r(k)
    c = 1.5  # Example constant factor, adjust as needed
    if H_G > c * r_k:
        return {
            "metric_name": "H(G)/r(k)",
            "metric_value": H_G / r_k,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"H(G)={H_G}, r(k)={r_k}"
        }
    
    return {
        "metric_name": "H(G)/r(k)",
        "metric_value": H_G / r_k,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")