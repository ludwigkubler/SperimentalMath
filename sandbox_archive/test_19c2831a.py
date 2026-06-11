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
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, n):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
        return A

    def matrix_rank(A):
        rank = 0
        A = gaussian_elimination(A)
        for row in A:
            if any(row):
                rank += 1
        return rank

    def construct_quasigroup(n, formula):
        # Construct a quasigroup from a CNF formula
        # This is a simplified mapping and may not accurately represent the conjecture
        q = [[0] * n for _ in range(n)]
        for clause in formula:
            for i in range(n):
                for j in range(i+1, n):
                    if (i, j) not in q and (j, i) not in q:
                        q[i][j] = 1
                        break
        return q

    def resolution_width(formula):
        # Simplified resolution width calculation
        # This is a placeholder and may not accurately represent the conjecture
        return len(formula)

    n_values = [10, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = [[random.choice([1, -1]) * random.randint(1, n) for _ in range(n)] for _ in range(random.randint(5, 10))]
        q = construct_quasigroup(n, formula)
        order = matrix_rank(q)
        width = resolution_width(formula)
        results.append({
            "n": n,
            "order": order,
            "width": width
        })
    
    if len(results) < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    correlation = 0
    n_sum = sum(result["n"] for result in results)
    order_sum = sum(result["order"] for result in results)
    width_sum = sum(result["width"] for result in results)
    n_order_product_sum = sum(result["n"] * result["order"] for result in results)
    n_width_product_sum = sum(result["n"] * result["width"] for result in results)
    
    n_mean = n_sum / len(results)
    order_mean = order_sum / len(results)
    width_mean = width_sum / len(results)
    
    numerator = n_order_product_sum - n_mean * order_mean
    denominator = math.sqrt((sum(result["n"]**2 for result in results) - n_mean**2) * (order_sum**2 - order_mean**2))
    
    if denominator == 0:
        correlation = None
    else:
        correlation = numerator / denominator
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": correlation is not None and abs(correlation) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std = math.sqrt(sum((r["metric_value"] - mean)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any("conjecture_holds" in r and not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "conjecture_holds" in result and not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_threshold_not_met\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")