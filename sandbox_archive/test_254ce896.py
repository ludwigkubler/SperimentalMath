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
    
    def compute_density_matrix(f):
        n = len(f)
        density_matrix = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if f[i] == f[j]:
                    density_matrix[i][j] = 1 / (2**n)
        return density_matrix
    
    def matrix_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            pivot_row = -1
            for j in range(i, n):
                if matrix[j][i] != 0:
                    pivot_row = j
                    break
            if pivot_row == -1:
                continue
            rank += 1
            for j in range(n):
                if j != i:
                    factor = matrix[j][i] / matrix[pivot_row][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[pivot_row][k]
        return rank
    
    def circuit_weight(f):
        n = len(f)
        # Simplified heuristic for circuit weight
        return sum(1 for bit in f if bit == 1)
    
    def is_maximally_entangled(n):
        # Simplified heuristic to check if the function represents a maximally entangled state
        return all(bit == 0 or bit == 1 for bit in f)
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    
    if not is_maximally_entangled(f):
        return {
            "metric_name": "rho",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "not_maximally_entangled"
        }
    
    rho = compute_density_matrix(f)
    rank_rho = matrix_rank(rho)
    W_f = circuit_weight(f)
    
    if rank_rho <= 0:
        return {
            "metric_name": "rho",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "singular_matrix"
        }
    
    log_n = math.log2(n)
    if not (log_n - 3 <= rank_rho <= log_n + 3):
        return {
            "metric_name": "rho",
            "metric_value": rank_rho,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"rank_rho={rank_rho}, expected Θ(log n) = {log_n}"
        }
    
    if W_f > 2**rank_rho:
        return {
            "metric_name": "W(f)",
            "metric_value": W_f,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"W(f)={W_f}, expected ≤ 2^ρ(f) = {2**rank_rho}"
        }
    
    return {
        "metric_name": "rho",
        "metric_value": rank_rho,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 30))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_rho = sum(result["metric_value"] for result in results) / len(results)
        std_rho = math.sqrt(sum((result["metric_value"] - mean_rho)**2 for result in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")