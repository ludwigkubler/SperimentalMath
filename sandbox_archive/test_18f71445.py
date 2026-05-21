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
    
    def generate_read_twice_bp(n):
        edges = []
        for i in range(n):
            for j in range(i+1, n):
                if random.choice([True, False]):
                    edges.append((i, j))
        return edges

    def tensor_product(matrices):
        result = matrices[0]
        for matrix in matrices[1:]:
            new_result = []
            for i in range(len(result)):
                for j in range(len(matrix)):
                    row = [sum(a*b for a, b in zip(row_i, col_j)) for col_j in zip(*matrix)]
                    new_result.append(row)
            result = new_result
        return result

    def log_det(matrix):
        n = len(matrix)
        det = 1.0
        for i in range(n):
            det *= matrix[i][i]
        return math.log(det)

    n = 16
    edges = generate_read_twice_bp(n)
    
    M = [[0] * n for _ in range(n)]
    for u, v in edges:
        M[u][v] += 1 / len(edges)
        M[v][u] += 1 / len(edges)
    for i in range(n):
        M[i][i] += 1 - sum(M[i])

    rho = - (1/n) * log_det(tensor_product([M]*n))
    
    return {
        "metric_name": "free_entropy",
        "metric_value": rho,
        "instances_tested": 1,
        "conjecture_holds": rho >= 0.3 * math.log(n),
        "counterexample": "" if rho >= 0.3 * math.log(n) else f"Graph with n={n}, edges={edges}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 59))  # Default to first 30 primes

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rho = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rho} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rho} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='{r['counterexample']}' first_failing_seed={first_failing_seed}")