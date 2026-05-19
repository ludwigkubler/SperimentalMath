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
    
    def generate_expander_graph(n):
        if n <= 1:
            return []
        G = [[0] * n for _ in range(n)]
        for i in range(1, n):
            neighbors = random.sample(range(i), min(i-1, 3))
            for j in neighbors:
                G[i][j] = G[j][i] = 1
        return G
    
    def tensor_product(A, B):
        m, n = len(A), len(A[0])
        p, q = len(B), len(B[0])
        result = [[0] * (n * q) for _ in range(m * p)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    for l in range(q):
                        result[i*p + k][j*q + l] = A[i][j] * B[k][l]
        return result
    
    def count_irreducible_components(matrix):
        n = len(matrix)
        if n == 0:
            return 0
        components = set()
        for i in range(n):
            for j in range(i+1, n):
                if matrix[i][j] != 0:
                    components.add((i, j))
        return len(components)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_components = 0
    instances_tested = 0
    
    for n in n_values:
        G = generate_expander_graph(n)
        A = tensor_product(G, G)
        components = count_irreducible_components(A)
        total_components += components
        instances_tested += 1
    
    metric_value = total_components / len(n_values)
    conjecture_holds = metric_value >= 2**30
    counterexample = "" if conjecture_holds else f"n={n}, components={components}"
    
    return {
        "metric_name": "irreducible_components",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample_desc = results[results.index(next(r for r in results if not r["conjecture_holds"]))]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")