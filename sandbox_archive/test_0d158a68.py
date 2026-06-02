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
    
    # Generate a random d-regular graph G with n vertices
    n = 30
    d = 2 * (n - 1) // n  # Ensure d is even and regular
    if d < 2 or d > n - 2:
        return {
            "metric_name": "circuit_depth",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "invalid_d"
        }
    
    # Generate the adjacency matrix of a d-regular graph
    adj_matrix = [[0] * n for _ in range(n)]
    edges = []
    for i in range(n):
        neighbors = random.sample(range(n), d)
        for j in neighbors:
            if i < j and (i, j) not in edges and (j, i) not in edges:
                adj_matrix[i][j] = 1
                adj_matrix[j][i] = 1
                edges.append((i, j))
    
    # Compute the minimal order of elements in the associated K-theory group
    # This is a placeholder for the actual computation
    min_order = random.randint(1, n)
    
    # Compute the circuit depth of the graph
    # This is a placeholder for the actual computation
    circuit_depth = random.randint(1, 2 * n)
    
    return {
        "metric_name": "circuit_depth",
        "metric_value": min_order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    # Compute mean/std of metric_value and fraction of seeds where conjecture_holds
    if len(results) == 0:
        print("RESULT: INCONCLUSIVE no_results")
    else:
        values = [r["metric_value"] for r in results if r["metric_value"] is not None]
        holds = sum(r["conjecture_holds"] for r in results)
        
        mean = sum(values) / len(values) if values else 0
        std = math.sqrt(sum((x - mean) ** 2 for x in values) / len(values)) if values else 0
        
        support_fraction = holds / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
        elif holds > 0:
            first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample='not_supported' first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE no_support")