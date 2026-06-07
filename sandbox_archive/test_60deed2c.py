# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, permutations

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
            factor = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if i != j:
                    factor = Fraction(A[j][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def polynomial_from_cnf(phi):
        n = len(phi)
        poly = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in phi:
            for i, j in combinations(range(n), 2):
                if (i+1, j+1) not in clause and (j+1, i+1) not in clause:
                    poly[i][j] += 1
        return poly

    def dpll(phi):
        def solve(assignment):
            if len(assignment) == n:
                for clause in phi:
                    if all(lit not in assignment or assignment[lit] != val for lit, val in clause):
                        return False
                return True
            var = next((i for i in range(n) if i+1 not in assignment), None)
            if var is None:
                return True
            assignment[var+1] = True
            if solve(assignment):
                return True
            assignment[var+1] = False
            if solve(assignment):
                return True
            del assignment[var+1]
            return False
        
        return solve({})

    def mhdrank(poly):
        rank = 0
        for row in poly:
            if any(x != 0 for x in row):
                rank += 1
        return rank

    n_max = 40
    instances_tested = 0
    metric_values = []
    
    for n in range(5, 41):
        phi = [random.sample(range(1, n+1), random.randint(1, n)) for _ in range(n)]
        poly = polynomial_from_cnf(phi)
        try:
            rank = mhdrank(poly)
            width = dpll(phi)
            metric_values.append((rank, width))
            instances_tested += 1
        except ZeroDivisionError:
            continue
    
    if not metric_values:
        return {
            "metric_name": "mhdrank vs. w_DPLL",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    rank_values, width_values = zip(*metric_values)
    correlation_coefficient = sum((rank - mean_rank) * (width - mean_width) for rank, width in metric_values) / instances_tested
    mean_absolute_difference = sum(abs(rank - width) for rank, width in metric_values) / instances_tested
    
    return {
        "metric_name": "mhdrank vs. w_DPLL",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_absolute_difference <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 17 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")