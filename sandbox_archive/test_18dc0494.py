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
    n = random.randint(5, 40)
    
    # Generate a random triangle detection instance
    graph = {i: set() for i in range(n)}
    edges = []
    for _ in range(random.randint(1, n * (n - 1) // 2)):
        u, v = random.sample(range(n), 2)
        if u != v and u not in graph[v]:
            graph[u].add(v)
            graph[v].add(u)
            edges.append((u, v))
    
    # Compute the incidence matrix
    I = [[0] * n for _ in range(n)]
    for u, v in edges:
        I[u][v] = 1
        I[v][u] = 1
    
    # Compute the tropicalized Lie algebra representation rank
    rank = compute_tropical_rank(I)
    
    # Compute communication complexity (simplified as number of edges)
    C_I = len(edges)
    
    # Define r(n) = Θ(log²(n))
    r_n = math.log2(n) ** 2
    
    # Check if the conjecture holds
    conjecture_holds = rank > r_n
    counterexample = "" if conjecture_holds else "r(n) not exceeded"
    
    return {
        "metric_name": "Rank of Tropicalized Lie Algebra",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def compute_tropical_rank(matrix):
    n = len(matrix)
    # Gaussian elimination to find the rank
    for i in range(n):
        if matrix[i][i] == 0:
            # Find a row with non-zero pivot in the same column
            found = False
            for j in range(i + 1, n):
                if matrix[j][i] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    found = True
                    break
            if not found:
                continue
        
        # Eliminate the pivot in all other rows
        for j in range(n):
            if i != j and matrix[j][i] != 0:
                factor = -matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] += factor * matrix[i][k]
    
    # Count the number of non-zero rows
    rank = sum(1 for row in matrix if any(x != 0 for x in row))
    return rank

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"r(n) not exceeded\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")