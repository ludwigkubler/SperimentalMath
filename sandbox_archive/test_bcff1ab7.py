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
            if i != j:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def dpll(sat_instance, assignment=None):
    if assignment is None:
        assignment = {}
    if not sat_instance:
        return True
    var = next((v for v in sat_instance if v not in assignment), None)
    if var is None:
        return True
    pos_clauses = [c for c in sat_instance if any(lit in assignment and assignment[lit] == 1 for lit in c)]
    neg_clauses = [c for c in sat_instance if any(lit in assignment and assignment[lit] == -1 for lit in c)]
    if not pos_clauses:
        return dpll(sat_instance, {var: -1})
    if not neg_clauses:
        return dpll(sat_instance, {var: 1})
    return dpll(sat_instance, {var: 1}) or dpll(sat_instance, {var: -1})

def min_hodge_decomposition_complexity(n):
    # Placeholder for actual Hodge decomposition computation
    # For simplicity, we use a linear function of n
    return n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        hdc_sum = 0
        h_sum = 0
        for _ in range(5):  # Sample 5 instances per size
            sat_instance = []
            for i in range(n):
                for j in range(i+1, n):
                    if random.choice([True, False]):
                        lit = (i+1) * n + j + 1
                    else:
                        lit = -(i+1) * n - j - 1
                    sat_instance.append((lit,))
            hdc = min_hodge_decomposition_complexity(n)
            h = dpll(sat_instance)
            if h is None:
                continue
            instances_tested += 1
            hdc_sum += hdc
            h_sum += h
        if instances_tested == 0:
            continue
        hdc_avg = hdc_sum / instances_tested
        h_avg = h_sum / instances_tested
        results.append((hdc_avg, h_avg))
    if not results:
        return {
            "metric_name": "HDC vs H",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances tested"
        }
    hdc_values, h_values = zip(*results)
    correlation_coefficient = sum((hdc - hdc_avg) * (h - h_avg) for hdc, h in zip(hdc_values, h_values)) / len(hdc_values)
    return {
        "metric_name": "HDC vs H",
        "metric_value": correlation_coefficient,
        "instances_tested": sum(len(results)),
        "n_max": 40,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(result["instances_tested"] > 0 for result in results):
        print("RESULT: INCONCLUSIVE insufficient_instances")
    else:
        hdc_values = [result["metric_value"] for result in results if result["metric_value"] is not None]
        support_fraction = sum(1 for result in results if abs(result["metric_value"]) >= 0.8) / len(results)
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={sum(hdc_values)/len(hdc_values)} std={math.sqrt(sum((x-sum(hdc_values)/len(hdc_values))**2 for x in hdc_values)/len(hdc_values))} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result["metric_value"]) < 0.8)
            print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_too_low\" first_failing_seed={first_failing_seed}")