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
    
    def density_matrix(f):
        n = len(f)
        rho = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if f[i] == f[j]:
                    rho[i][j] += 1
        return rho
    
    def min_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if matrix[i][i] != 0:
                rank += 1
                for j in range(i + 1, n):
                    matrix[j][i] /= matrix[i][i]
                for j in range(n):
                    if j != i:
                        for k in range(i + 1, n):
                            matrix[j][k] -= matrix[j][i] * matrix[i][k]
        return rank
    
    def circuit_weight(f):
        # Placeholder function for actual circuit weight calculation
        return len(f)
    
    n = random.randint(5, 30)
    f = generate_boolean_function(n)
    rho = density_matrix(f)
    rank = min_rank(rho)
    W_f = circuit_weight(f)
    
    log_n = math.log2(n)
    if rank < log_n * (1/3) or rank > log_n * (4/3):
        return {
            "metric_name": "min_rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Rank {rank} is not within a factor of 3 from log n = {log_n}"
        }
    if W_f > 2 ** rank:
        return {
            "metric_name": "circuit_weight",
            "metric_value": W_f,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Circuit weight {W_f} exceeds 2^rank = {2 ** rank}"
        }
    
    return {
        "metric_name": "min_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")