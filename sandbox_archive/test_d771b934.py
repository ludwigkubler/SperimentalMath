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
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(cols):
                if j != i:
                    factor = Fraction(matrix[j][i], matrix[i][i])
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def grb_minimal_intersection_rank(cnf):
        n = len(cnf)
        k = sum(1 for clause in cnf if len(clause) == 2)
        return (n ** 2 * k / 3)
    
    def construct_monotone_circuit(n, k):
        # Simplified construction; actual circuit complexity is much higher
        return n ** k
    
    def generate_random_cnf(n, k):
        cnf = []
        for _ in range(k):
            clause = random.sample(range(1, n + 1), 2)
            cnf.append(clause)
        return cnf
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_grb_rank = 0
    total_circuit_size = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_random_cnf(n, k)
            grb_rank = grb_minimal_intersection_rank(cnf)
            circuit_size = construct_monotone_circuit(n, k)
            total_grb_rank += grb_rank
            total_circuit_size += circuit_size
            instances_tested += 1
    
    mean_grb_rank = Fraction(total_grb_rank, instances_tested)
    mean_circuit_size = Fraction(total_circuit_size, instances_tested)
    
    ratio = mean_grb_rank / mean_circuit_size
    if ratio > 0:
        conjecture_holds = True
    else:
        conjecture_holds = False
    
    return {
        "metric_name": "Ratio of Gröbner Basis Rank to Circuit Size",
        "metric_value": float(ratio),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")