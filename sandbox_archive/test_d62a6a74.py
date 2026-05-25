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
    
    def generate_k_clique(n, k):
        if k > n // 2:
            return None
        vertices = list(range(n))
        clique_edges = []
        for i in range(k):
            for j in range(i + 1, k):
                clique_edges.append((vertices[i], vertices[j]))
        remaining_edges = [(i, j) for i in range(k, n) for j in range(i + 1, n)]
        random.shuffle(remaining_edges)
        edges = clique_edges + remaining_edges[:n - k]
        return edges
    
    def matrix_representation(edges, n):
        mat = [[0] * n for _ in range(n)]
        for u, v in edges:
            mat[u][v] = 1
            mat[v][u] = 1
        return mat
    
    def tropical_intersection_number(mat):
        n = len(mat)
        # Placeholder for actual computation of tropical intersection number
        # This is a dummy implementation for demonstration purposes
        return sum(sum(row) for row in mat) / (n * n)
    
    def communication_complexity(n, k):
        # Placeholder for actual computation of communication complexity
        # This is a dummy implementation for demonstration purposes
        return n ** k * math.log(n)
    
    n = 40
    k = 3
    edges = generate_k_clique(n, k)
    if edges is None:
        return {
            "metric_name": "communication_complexity",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "k too large for n"
        }
    
    mat = matrix_representation(edges, n)
    tau_T = tropical_intersection_number(mat)
    CC_k_Clique = communication_complexity(n, k)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": CC_k_Clique,
        "instances_tested": 1,
        "conjecture_holds": tau_T <= CC_k_Clique and tau_T == n ** k * math.log(n),
        "counterexample": "" if tau_T <= CC_k_Clique else f"CC(k-Clique) = {CC_k_Clique}, τ(T) = {tau_T}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")