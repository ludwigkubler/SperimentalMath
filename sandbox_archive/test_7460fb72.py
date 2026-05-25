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
    
    def generate_random_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def incidence_matrix(graph, n):
        mat = [[0] * n for _ in range(n)]
        for u, v in graph:
            mat[u][v] = 1
            mat[v][u] = 1
        return mat
    
    def tropical_determinant(mat):
        if len(mat) == 0 or len(mat[0]) == 0:
            return 0
        n = len(mat)
        max_entries = [[-math.inf] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                max_entries[i][j] = max(max_entries[i][j], mat[i][j])
        
        det = 1
        for i in range(n):
            det *= max_entries[i][i]
        return det
    
    def tropical_euler_characteristic(graph, n):
        mat = incidence_matrix(graph, n)
        det = tropical_determinant(mat)
        if det <= 0:
            return -math.inf
        return math.log(det)
    
    def ac0_parity_depth(graph, n):
        # Placeholder for actual AC0 parity depth computation
        # This is a dummy implementation for testing purposes
        return random.randint(1, n)
    
    n = random.choice([10, 15, 20, 25, 30, 35, 40])
    graph = generate_random_graph(n)
    chi_t = tropical_euler_characteristic(graph, n)
    ac0_depth = ac0_parity_depth(graph, n)
    
    if chi_t == -math.inf:
        return {
            "metric_name": "tropical_euler_characteristic",
            "metric_value": chi_t,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "chi_t is negative infinity"
        }
    
    c = 0.5  # Placeholder constant for the lower bound
    if chi_t >= c * math.log(n):
        return {
            "metric_name": "tropical_euler_characteristic",
            "metric_value": chi_t,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "tropical_euler_characteristic",
            "metric_value": chi_t,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"chi_t ({chi_t}) < c * log(n) ({c * math.log(n)})"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"chi_t < c * log(n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")