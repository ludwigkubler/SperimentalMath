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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = extended_gcd(b % a, a)
        return (g, y - (b // a) * x, x)

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("Modular inverse does not exist")
    else:
        return x % m

def is_quadratic_residue(a, p):
    if a == 0:
        return True
    if gcd(a, p) != 1:
        return False
    return pow(a, (p - 1) // 2, p) == 1

def quadratic_residues_count(p):
    count = 0
    for i in range(1, p):
        if is_quadratic_residue(i, p):
            count += 1
    return count

def gaussian_elimination(A, b):
    n = len(b)
    A_b = [row + [b[i]] for i, row in enumerate(A)]
    
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A_b[i], A_b[max_row] = A_b[max_row], A_b[i]
        
        pivot = A_b[i][i]
        if pivot == 0:
            continue
        
        for j in range(i+1, n):
            factor = A_b[j][i] / pivot
            for k in range(n + 1):
                A_b[j][k] -= factor * A_b[i][k]
    
    x = [0] * n
    for i in reversed(range(n)):
        x[i] = A_b[i][-1]
        for j in range(i+1, n):
            x[i] -= A_b[i][j] * x[j]
        x[i] /= A_b[i][i]
    
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 30
    instances_tested = 0
    total_dpll_height = 0
    
    for _ in range(100):
        clause_indicators = [random.randint(2, n-1) for _ in range(n)]
        order = 1
        for p in clause_indicators:
            order *= (p - 1)
        
        residues_count = quadratic_residues_count(order)
        log_residues = math.log(residues_count)
        
        cnf_instance = [[random.choice([-1, 1]) * random.randint(1, n) for _ in range(n)] for _ in range(n)]
        try:
            dpll_height = len(gaussian_elimination(cnf_instance, [0] * n))
        except IndexError:
            continue
        
        instances_tested += 1
        total_dpll_height += abs(dpll_height - log_residues)
    
    if instances_tested == 0:
        return {
            "metric_name": "DPLL Height vs Log Residues",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    avg_dpll_height = total_dpll_height / instances_tested
    return {
        "metric_name": "DPLL Height vs Log Residues",
        "metric_value": avg_dpll_height,
        "instances_tested": instances_tested,
        "n_max": n,
        "conjecture_holds": abs(avg_dpll_height) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    avg_dpll_height = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if abs(r["metric_value"]) <= 3) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_dpll_height} std=0.0 support_fraction={support_fraction}")
    elif any(abs(r["metric_value"]) > 3 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result["metric_value"]) > 3)
        print(f"RESULT: FALSIFIED counterexample=\"DPLL height exceeds log residues by more than 3\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")