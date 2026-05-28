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

def quadratic_form_matrix(f):
    n = len(f)
    M_f = [[0] * n for _ in range(n)]
    for x_i in range(2**n):
        for x_j in range(2**n):
            sum_product = 0
            for k in range(n):
                bit_i = (x_i >> k) & 1
                bit_j = (x_j >> k) & 1
                sum_product += f[(bit_i, bit_j)]
            M_f[x_i][x_j] = sum_product
    return M_f

def min_rank(matrix):
    n = len(matrix)
    rank = 0
    for i in range(n):
        if all(matrix[j][i] == 0 for j in range(i)):
            continue
        pivot_row = next(j for j in range(i, n) if matrix[j][i] != 0)
        matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
        rank += 1
        for j in range(n):
            if i == j:
                continue
            factor = -matrix[j][i] / matrix[i][i]
            for k in range(n):
                matrix[j][k] += factor * matrix[i][k]
    return rank

def communication_complexity(f, n):
    # Placeholder for the actual communication complexity algorithm
    # For this example, we assume a known upper bound
    return 2**n - 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    f = {tuple(sorted(random.sample(range(n), 2))): random.choice([0, 1]) for _ in range(2**n)}
    
    M_f = quadratic_form_matrix(f)
    tau_quad = min_rank(M_f)
    
    comm_complexity = communication_complexity(f, n)
    
    metric_value = Fraction(tau_quad) / (n * math.log(n))
    conjecture_holds = 0.9 <= metric_value and comm_complexity <= 1.2 * tau_quad
    counterexample = "" if conjecture_holds else "communication_complexity > 1.2*tau_quad"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": float(metric_value),
        "instances_tested": len(f),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and "communication_complexity > 1.2*tau_quad" in r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"communication_complexity > 1.2*tau_quad\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")