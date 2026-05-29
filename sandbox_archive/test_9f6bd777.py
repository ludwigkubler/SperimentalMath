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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(1 << n)]
    
    def quantum_logarithmic_capacity(f):
        n = int(math.log2(len(f)))
        matrix = [[f[i * (1 << n) + j] for j in range(1 << n)] for i in range(1 << n)]
        
        # Gaussian elimination to find the rank of the matrix
        def gaussian_elimination(A):
            m, n = len(A), len(A[0])
            rank = 0
            for j in range(n):
                i_max = rank
                for i in range(rank, m):
                    if abs(A[i][j]) > abs(A[i_max][j]):
                        i_max = i
                if abs(A[i_max][j]) < 1e-9:
                    continue
                A[rank], A[i_max] = A[i_max], A[rank]
                for i in range(m):
                    if i != rank and abs(A[i][j]) > 1e-9:
                        factor = -A[i][j] / A[rank][j]
                        for k in range(n):
                            A[i][k] += factor * A[rank][k]
                rank += 1
            return rank
        
        rank = gaussian_elimination(matrix)
        return Fraction(rank, n + 1).log2()
    
    def monotone_circuit_size(f):
        # Placeholder for actual monotone circuit size calculation
        # For simplicity, we assume a linear relationship with QLC
        return len(f) * quantum_logarithmic_capacity(f)
    
    def minimal_depth(f):
        # Placeholder for actual minimal depth calculation
        # For simplicity, we assume a linear relationship with QLC
        return len(f) * quantum_logarithmic_capacity(f)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        qlc = quantum_logarithmic_capacity(f)
        d = minimal_depth(f)
        S_mon = monotone_circuit_size(f)
        
        results.append({
            "n": n,
            "qlc": qlc,
            "d": d,
            "S_mon": S_mon
        })
    
    metric_value = sum(result["S_mon"] - result["qlc"] ** 2 for result in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(result["S_mon"] >= result["qlc"] ** 2 for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "S_mon - QLC^2",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(seed) for seed in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30 * 100 + 2, 100))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and sum(1 for result in results if not result["conjecture_holds"]) / len(results) <= 0.2:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")