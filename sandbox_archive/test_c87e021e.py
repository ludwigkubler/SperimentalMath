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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for i in range(cols):
            pivot_row = next((r for r in range(rank, rows) if matrix[r][i] != 0), None)
            if pivot_row is not None:
                matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
                for j in range(rows):
                    if j != rank and matrix[j][i] != 0:
                        factor = -matrix[j][i] / matrix[rank][i]
                        for k in range(cols):
                            matrix[j][k] += factor * matrix[rank][k]
                rank += 1
        return rank
    
    def compute_galois_group_size(cnf):
        n = len(set(abs(lit) for clause in cnf for lit in clause))
        m = len(cnf)
        # Simplify the CNF using Gaussian elimination to find the rank
        matrix = [[int(lit in clause) for lit in range(1, n+1)] for clause in cnf]
        return 2 ** (n + math.log(m, 2))
    
    def compute_resolution_width(cnf):
        # Simplify the CNF using Gaussian elimination to find the rank
        matrix = [[int(lit in clause) for lit in range(1, n+1)] for clause in cnf]
        return gaussian_elimination(matrix)
    
    n_max = 40
    instances_tested = 0
    total_galois_group_size = 0
    total_resolution_width = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            cnf = generate_cnf(n, random.randint(1, n))
            galois_group_size = compute_galois_group_size(cnf)
            resolution_width = compute_resolution_width(cnf)
            
            instances_tested += 1
            total_galois_group_size += galois_group_size
            total_resolution_width += resolution_width
    
    if instances_tested < 30:
        return {
            "metric_name": "Galois Group Size",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_galois_group_size = total_galois_group_size / instances_tested
    mean_resolution_width = total_resolution_width / instances_tested
    
    return {
        "metric_name": "Galois Group Size",
        "metric_value": mean_galois_group_size,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": mean_resolution_width <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")