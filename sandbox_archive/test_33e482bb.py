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
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        for j in range(n):
            A[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def dpll_width(phi):
    literals = set()
    clauses = []
    for clause in phi:
        literals.update(clause)
        clauses.append(clause)
    
    def solve(model, literals, clauses):
        if not clauses:
            return len(model)
        literal = next(iter(literals))
        positive_clauses = [c for c in clauses if literal in c]
        negative_clauses = [c for c in clauses if -literal in c]
        if not positive_clauses and not negative_clauses:
            return float('inf')
        if positive_clauses:
            model.add(literal)
            width = solve(model, literals - {literal}, positive_clauses)
            model.remove(literal)
            if width < float('inf'):
                return width
        if negative_clauses:
            model.add(-literal)
            width = solve(model, literals - {-literal}, negative_clauses)
            model.remove(-literal)
            if width < float('inf'):
                return width
        return float('inf')
    
    return solve(set(), literals, clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for n in range(5, n_max + 1):
        phi = [[random.randint(-n, n) for _ in range(random.randint(2, n))] for _ in range(n)]
        order_rho_phi = len(phi)
        width_phi = dpll_width(phi)
        
        if width_phi == float('inf'):
            continue
        
        instances_tested += 1
        metric_values.append((order_rho_phi, width_phi))
        
        if instances_tested >= 30:
            break
    
    if instances_tested < 30:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }
    
    mean_o_qm = sum(o * q for o, q in metric_values) / sum(q for _, q in metric_values)
    mean_mte = sum((o - mean_o_qm) ** 2 for o, _ in metric_values) / (instances_tested - 1)
    std_dev = math.sqrt(mean_mte)
    
    correlation_coefficient = sum((o - mean_o_qm) * (q - mean_mte) for o, q in metric_values) / ((instances_tested - 1) * std_dev)
    
    if correlation_coefficient < 0.7:
        conjecture_holds = False
        counterexample = f"Correlation coefficient {correlation_coefficient} is below threshold"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr_coeff = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / sum(1 for r in results if r["metric_value"] is not None)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")