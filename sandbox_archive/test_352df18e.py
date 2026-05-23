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
    
    def tseitin_formula(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for i in range(m):
            clause = [random.choice(variables)]
            if random.choice([True, False]):
                clause.append(-random.choice(variables))
            clauses.append(clause)
        return variables, clauses
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                return None
            for j in range(i + 1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def rank(A):
        rref = gaussian_elimination(A)
        if rref is None:
            return 0
        return sum(1 for row in rref if any(row))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(n**2 // 4, n**2)
        variables, clauses = tseitin_formula(n, m)
        A = [[0] * (n + 1) for _ in range(m)]
        for j, clause in enumerate(clauses):
            for var in clause:
                if var > 0:
                    A[j][var - 1] += 1
                else:
                    A[j][-1] -= 1
        
        min_rank = rank(A)
        results.append({
            "n": n,
            "m": m,
            "min_rank": min_rank
        })
    
    if not results:
        return {
            "metric_name": "Minimal Rank of Brauer Groups",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    min_rank_values = [result["min_rank"] for result in results]
    log_min_rank = [math.log(x) if x > 0 else -float('inf') for x in min_rank_values]
    m_values = [result["m"] for result in results]
    log_m_cubed = [math.log(m**3) for m in m_values]
    log_n_squared = [math.log(n**2) for n in n_values]
    
    # Fit a curve to log(min_rank) ~ log(m^(1/3)) * log^2(n)
    def linear_fit(x, y):
        if len(x) != len(y):
            return None
        x_mean = sum(x) / len(x)
        y_mean = sum(y) / len(y)
        numerator = sum((xi - x_mean) * (yi - y_mean) for xi, yi in zip(x, y))
        denominator = sum((xi - x_mean)**2 for xi in x)
        slope = numerator / denominator if denominator != 0 else None
        intercept = y_mean - slope * x_mean if slope is not None else None
        return slope, intercept
    
    slope, intercept = linear_fit(log_m_cubed, log_n_squared)
    
    f_n = lambda n: math.exp(intercept + slope * math.log(n**2))
    
    metric_value = sum(f_n(result["n"]) for result in results) / len(results)
    conjecture_holds = all(result["min_rank"] <= 1.5 * f_n(result["n"])**2 for result in results)
    counterexample = "" if conjecture_holds else "f(n) too large"
    
    return {
        "metric_name": "Minimal Rank of Brauer Groups",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*37, 127))[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
        elif any(r["conjecture_holds"] for r in results):
            print(f"RESULT: FALSIFIED counterexample=\"f(n) too large\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
        else:
            print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE some trials had None metric_value")