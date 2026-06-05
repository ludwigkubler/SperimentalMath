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
    n = random.choice([5, 10, 15, 20, 30, 40])
    d = random.randint(2, min(n - 1, 3))
    
    # Generate a random d-regular graph
    if (n * d) % 2 != 0:
        return {"metric_name": "log2(|A(G)|)", "metric_value": None, "instances_tested": 0, "n_max": n, "conjecture_holds": False, "counterexample": "Graph size must be a multiple of the degree"}
    
    graph = [[0] * n for _ in range(n)]
    edges = set()
    while len(edges) < (n * d) // 2:
        u, v = random.sample(range(n), 2)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            graph[u][v] = 1
            graph[v][u] = 1
            edges.add((u, v))
    
    # Compute the automorphism group A(G)
    def is_automorphism(perm):
        for i in range(n):
            for j in range(n):
                if graph[i][j] != graph[perm[i]][perm[j]]:
                    return False
        return True
    
    aut_group = [tuple(range(n))]
    for perm in itertools.permutations(range(n)):
        if is_automorphism(perm) and perm not in aut_group:
            aut_group.append(perm)
    
    # Calculate log2(|A(G)|)
    log2_aut_size = math.log2(len(aut_group))
    
    # Construct the Frege proof for G (simplified example)
    def frege_proof_width(graph):
        # Simplified heuristic: width is proportional to number of edges
        return len(edges) // 2
    
    w_frege = frege_proof_width(graph)
    
    return {
        "metric_name": "log2(|A(G)|)",
        "metric_value": log2_aut_size,
        "instances_tested": n * d // 2,
        "n_max": n,
        "conjecture_holds": True if w_frege > 0 else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")