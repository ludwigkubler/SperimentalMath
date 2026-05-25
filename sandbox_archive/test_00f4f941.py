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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_quandle_invariant(f):
        n = int(math.log2(len(f)))
        q = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            for j in range(n + 1):
                if i == j:
                    q[i][j] = 1
                else:
                    q[i][j] = f[(i << n) | (1 << j) - 1]
        return q
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                return None
            for j in range(i + 1, n):
                matrix[i][j] /= matrix[i][i]
            for k in range(m):
                if k != i and matrix[k][i] != 0:
                    for j in range(i, n):
                        matrix[k][j] -= matrix[i][j] * matrix[k][i]
        return matrix
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        r = 0
        for i in range(n):
            if any(matrix[j][i] != 0 for j in range(r)):
                r += 1
        return r
    
    def min_ac0_k_distance_circuit(f):
        # Placeholder function to simulate the computation of AC^0-k-distance circuit size
        n = int(math.log2(len(f)))
        return random.randint(1, 2**n)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_boolean_function(n)
    q = compute_quandle_invariant(f)
    rank_q = rank(gaussian_elimination(q))
    ac0_k_distance_circuit_size = min_ac0_k_distance_circuit(f)
    
    c = 1.0
    bound = c * n * math.log(n)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank_q,
        "instances_tested": 1,
        "conjecture_holds": rank_q <= bound,
        "counterexample": "" if rank_q <= bound else f"rank_q={rank_q} > {bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank_q > c * n * log(n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")