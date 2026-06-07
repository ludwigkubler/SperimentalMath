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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def characteristic_polynomial(f):
        n = len(f)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if (i & (1 << j)) == 0:
                    A[i][j] = f[(i ^ (1 << j))]
                else:
                    A[i][j] = -f[(i ^ (1 << j))]
        return A
    
    def adjoint_group_order(A):
        n = len(A)
        I = [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]
        B = [row[:] for row in A]
        k = 0
        while k < n:
            max_row = max(range(k, n), key=lambda r: abs(B[r][k]))
            B[k], B[max_row] = B[max_row], B[k]
            if B[k][k] == 0:
                return float('inf')
            for j in range(n):
                B[k][j] /= B[k][k]
            for i in range(n):
                if i != k:
                    factor = B[i][k]
                    for j in range(n):
                        B[i][j] -= factor * B[k][j]
            k += 1
        return n
    
    def circuit_entanglement_complexity(f):
        # Placeholder function; actual implementation needed
        n = len(f)
        return n  # This is a dummy value for testing purposes
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        A = characteristic_polynomial(f)
        omega = adjoint_group_order(A)
        e_f = circuit_entanglement_complexity(f)
        results.append({
            "n": n,
            "omega": omega,
            "e_f": e_f
        })
    
    if not results:
        return {
            "metric_name": "Spearman's rank correlation coefficient",
            "metric_value": float('nan'),
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    omega_values = [r["omega"] for r in results]
    e_f_values = [r["e_f"] for r in results]
    
    def rank_correlation(x, y):
        n = len(x)
        sorted_x = sorted(range(n), key=lambda i: x[i])
        sorted_y = sorted(range(n), key=lambda i: y[i])
        rank_x = [sorted_x.index(i) for i in range(n)]
        rank_y = [sorted_y.index(i) for i in range(n)]
        return sum((rank_x[i] - rank_y[i]) ** 2 for i in range(n)) / (n * (n**2 - 1))
    
    r = rank_correlation(omega_values, e_f_values)
    
    return {
        "metric_name": "Spearman's rank correlation coefficient",
        "metric_value": r,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": r >= 0.7,
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
    
    if not all(r["conjecture_holds"] for r in results):
        counterexample = next((r for r in results if not r["conjecture_holds"]), None)
        first_failing_seed = counterexample["seed"]
        RESULT = f"RESULT: FALSIFIED counterexample=\"Spearman's rank correlation coefficient < 0.7\" first_failing_seed={first_failing_seed}"
    else:
        mean_r = sum(r["metric_value"] for r in results) / len(results)
        std_r = math.sqrt(sum((r["metric_value"] - mean_r) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        RESULT = f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}"
    
    print(RESULT)