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
    
    def generate_boolean_circuit(depth):
        if depth == 0:
            return random.choice([0, 1])
        else:
            left = generate_boolean_circuit(depth - 1)
            right = generate_boolean_circuit(depth - 1)
            return random.choice([left and right, left or right])
    
    def generate_tropicalized_affine_scheme(circuit):
        if isinstance(circuit, int):
            return [[circuit]]
        else:
            left = generate_tropicalized_affine_scheme(circuit[0])
            right = generate_tropicalized_affine_scheme(circuit[1])
            return [left[i] + right[i] for i in range(len(left))]
    
    def rank(A):
        if not A or not A[0]:
            return 0
        m, n = len(A), len(A[0])
        for col in range(n):
            pivot_row = None
            for row in range(m):
                if A[row][col] != 0:
                    pivot_row = row
                    break
            if pivot_row is None:
                continue
            for i in range(m):
                if i != pivot_row:
                    factor = A[i][col] / A[pivot_row][col]
                    for j in range(n):
                        A[i][j] -= factor * A[pivot_row][j]
        return sum(1 for row in A if any(x != 0 for x in row))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_boolean_circuit(n)
        A = generate_tropicalized_affine_scheme(circuit)
        r_A = rank(A)
        results.append({
            "n": n,
            "circuit_size": len(circuit),
            "rank": r_A
        })
    
    if not results:
        return {
            "metric_name": "Spearman's rank correlation",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    def spearman_rank_correlation(x, y):
        n = len(x)
        ranks_x = {v: i for i, v in enumerate(sorted(set(x)), start=1)}
        ranks_y = {v: i for i, v in enumerate(sorted(set(y)), start=1)}
        d_squared_sum = sum((ranks_x[x[i]] - ranks_y[y[i]]) ** 2 for i in range(n))
        return 1 - (6 * d_squared_sum) / (n * (n**2 - 1))
    
    x = [result["circuit_size"] for result in results]
    y = [result["rank"] for result in results]
    rho = spearman_rank_correlation(x, y)
    
    return {
        "metric_name": "Spearman's rank correlation",
        "metric_value": rho,
        "instances_tested": len(results),
        "conjecture_holds": rho >= 0.8 and all(rho_i >= 0.5 for rho_i in [spearman_rank_correlation([r["circuit_size"]], [r["rank"]]) for r in results]),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) if sys.argv[1:] else [2**i + 3**j for i in range(5) for j in range(5)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rho = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_rho = math.sqrt(sum((result["metric_value"] - mean_rho) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(rho is not None and rho >= 0.8 for rho in [result["metric_value"] for result in results]):
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    elif any(result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Spearman's rank correlation < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=not_enough_support")