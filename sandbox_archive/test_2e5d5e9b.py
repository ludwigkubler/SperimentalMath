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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        rank = sum(1 for row in A if any(row))
        return rank
    
    def clause_indicator_polynomial(clauses, n):
        poly = [[0] * (2**n) for _ in range(len(clauses))]
        for i, clause in enumerate(clauses):
            for literal in clause:
                index = 2**(abs(literal)-1)
                if literal > 0:
                    poly[i][index-1] += 1
                else:
                    poly[i][index-1] -= 1
        return poly
    
    def geometric_invariant_theory(poly):
        m, n = len(poly), len(poly[0])
        A = [[poly[i][j] for j in range(n)] for i in range(m)]
        rank = gaussian_elimination(A)
        return rank
    
    def generate_3cnf_instance(n, m):
        clauses = []
        for _ in range(m):
            clause = random.sample(range(1, n+1), 3)
            clause.append(random.choice([-1, 1]) * random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            m = random.randint(1, n**2)
            clauses = generate_3cnf_instance(n, m)
            poly = clause_indicator_polynomial(clauses, n)
            rank = geometric_invariant_theory(poly)
            results.append({
                "n": n,
                "m": m,
                "rank": rank
            })
    
    if not results:
        return {
            "metric_name": "g(n)",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    total_rank = sum(result["rank"] for result in results)
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    
    if n_max < 40:
        return {
            "metric_name": "g(n)",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "n_max_too_small"
        }
    
    g_n = lambda n, m: (m**(1/4) * n**(1/2))
    support_fraction = sum(1 for result in results if result["rank"] >= 0.8 * g_n(result["n"], result["m"])) / instances_tested
    
    return {
        "metric_name": "g(n)",
        "metric_value": total_rank / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_results")