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
    
    def generate_disjointness_instance(n):
        variables = list(range(n))
        clauses = []
        for _ in range(n):
            clause = random.sample(variables, 2)
            clauses.append(clause)
        return clauses
    
    def construct_polynomial(clauses):
        n = len(clauses)
        poly = [[0] * (n + 1) for _ in range(n + 1)]
        for i, (x, y) in enumerate(clauses):
            poly[x][y] = 1
            poly[y][x] = 1
        return poly
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                return None
            for j in range(i + 1, n):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n + 1):
                    matrix[j][k] -= factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def spearman_correlation(ranks, expected_ranks):
        n = len(ranks)
        d_squared_sum = sum((ranks[i] - expected_ranks[i]) ** 2 for i in range(n))
        rho_numerator = n * (n**2 - 1) - 6 * d_squared_sum
        rho_denominator = (n**2 - 1) * (2 * n**2 - 9 * n + 7)
        return rho_numerator / rho_denominator
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    instance = generate_disjointness_instance(n)
    poly = construct_polynomial(instance)
    rank = gaussian_elimination(poly)
    
    if rank is None:
        return {
            "metric_name": "minimal_rank",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "singular_matrix"
        }
    
    expected_ranks = [n**2] * n
    rho = spearman_correlation([rank], expected_ranks)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rho >= 0.7,
        "counterexample": "" if rho >= 0.7 else f"Spearman's rank correlation {rho} < 0.7"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_rank = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] != "" for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "counterexample" in result and result["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if 'counterexample' in r)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")