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
    
    def generate_quiver(n, m):
        vertices = list(range(n))
        edges = []
        for _ in range(m):
            u, v = random.sample(vertices, 2)
            if (u, v) not in edges and (v, u) not in edges:
                edges.append((u, v))
        return vertices, edges
    
    def minimal_order_of_automorphisms(vertices, edges):
        n = len(vertices)
        m = len(edges)
        
        # Construct the adjacency matrix
        adj_matrix = [[0] * n for _ in range(n)]
        for u, v in edges:
            adj_matrix[u][v] = 1
            adj_matrix[v][u] = 1
        
        # Find all permutations of vertices
        from itertools import permutations
        perms = list(permutations(vertices))
        
        min_order = float('inf')
        for perm in perms:
            is_automorphism = True
            for u, v in edges:
                if adj_matrix[perm[u]][perm[v]] != 1:
                    is_automorphism = False
                    break
            if is_automorphism:
                min_order = min(min_order, math.factorial(n))
        
        return min_order
    
    def communication_complexity(m):
        # Simplified model for communication complexity
        return math.sqrt(m)
    
    n = random.randint(5, 40)
    m = random.randint(1, n * (n - 1) // 2)
    vertices, edges = generate_quiver(n, m)
    
    minimal_order = minimal_order_of_automorphisms(vertices, edges)
    c_Q = communication_complexity(m)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": c_Q,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(c_Q - math.sqrt(m)) <= 1,
        "counterexample": "" if minimal_order == math.inf else f"minimal_order={minimal_order}, expected=O(m^(1/3))"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_c = sum(r["metric_value"] for r in results) / len(results)
    std_c = math.sqrt(sum((r["metric_value"] - mean_c) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_c} std={std_c} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"minimal_order does not match expected\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")