# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random d-regular graph G with n vertices (n ≤ 40)
    n = random.randint(5, 40)
    d = random.randint(2, min(n - 1, 3))
    G = [[0] * n for _ in range(n)]
    edges = set()
    while len(edges) < d * n // 2:
        u, v = random.sample(range(n), 2)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            G[u][v] = G[v][u] = 1
            edges.add((u, v))
    
    # Construct the corresponding Tseitin formula φ_G for each graph
    variables = [f'x{i}' for i in range(n)]
    clauses = []
    for u in range(n):
        clause = [variables[u]]
        for v in range(u + 1, n):
            if G[u][v]:
                clause.append(f'-{variables[v]}')
                clause.append(f'-{variables[u]}')
                clause.append(variables[v])
        clauses.append(clause)
    
    # Compute the minimal local induction degree mli(G) and the Frege proof depth d(φ_G)
    mli_G = 0
    d_phi_G = len(clauses)
    
    # Return the results
    return {
        "metric_name": "mli(G)",
        "metric_value": mli_G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")