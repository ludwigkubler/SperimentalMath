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
    
    def generate_d_regular_graph(n, d):
        if (d * n) % 2 != 0 or d < 1 or d >= n:
            return None
        graph = [[0] * n for _ in range(n)]
        edges = set()
        for i in range(n):
            neighbors = random.sample(range(n), d)
            for j in neighbors:
                if (i, j) not in edges and (j, i) not in edges:
                    graph[i][j] = 1
                    graph[j][i] = 1
                    edges.add((i, j))
        return graph

    def galois_group_order(n):
        if n == 2:
            return 2
        elif n == 3:
            return 6
        elif n == 4:
            return 24
        else:
            return None

    def resolution_proof_entanglement_complexity(graph):
        # Placeholder for actual computation
        # For simplicity, we use a dummy value that depends on the seed
        return random.random() * 10 + seed % 5

    n = random.randint(5, 40)
    d = random.randint(2, n-1)
    graph = generate_d_regular_graph(n, d)
    
    if graph is None:
        return {
            "metric_name": "ord(G)",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "invalid_d_regular_graph"
        }
    
    ord_G = galois_group_order(n)
    e_phi_G = resolution_proof_entanglement_complexity(graph)

    return {
        "metric_name": "ord(G)",
        "metric_value": ord_G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" not in r or r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if "conjecture_holds" not in r or r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")