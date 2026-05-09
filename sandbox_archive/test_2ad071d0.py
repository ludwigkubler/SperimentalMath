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

def fast_walsh_hadamard_transform(arr):
    n = len(arr)
    if n == 1:
        return arr
    even = fast_walsh_hadamard_transform(arr[0::2])
    odd = fast_walsh_hadamard_transform(arr[1::2])
    result = [0] * n
    for i in range(n // 2):
        result[i] = even[i] + odd[i]
        result[i + n // 2] = even[i] - odd[i]
    return result

def generate_kcnf(n, k):
    clauses = []
    variables = list(range(1, n + 1))
    for _ in range(k * n):
        clause = random.sample(variables, random.randint(1, n))
        if random.choice([True, False]):
            clause = [-v for v in clause]
        clauses.append(clause)
    return clauses

def dpll_solve(cnf):
    def solve(vars, assignment):
        if not cnf:
            return True
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            v = abs(unit_clause[0])
            sign = unit_clause[0] > 0
            if v in assignment and assignment[v] != sign:
                return False
            assignment[v] = sign
            cnf = [c for c in cnf if v not in c]
            if -v in cnf:
                cnf.remove([-v])
        pure_literal = next((v for v in range(1, len(assignment) + 1) if (v not in assignment and -v not in assignment)), None)
        if pure_literal is not None:
            sign = random.choice([True, False])
            assignment[pure_literal] = sign
            cnf = [c for c in cnf if pure_literal not in c]
            if -pure_literal in cnf:
                cnf.remove([-pure_literal])
        if len(assignment) == len(vars):
            return True
        v = next(v for v in range(1, len(assignment) + 1) if v not in assignment)
        return solve(vars, assignment | {v: True}) or solve(vars, assignment | {v: False})
    return solve(list(range(1, n + 1)), {})

def run_trial(seed):
    random.seed(seed)
    n = random.randint(5, 40)
    k = random.randint(1, min(n // 2, 10))
    cnf = generate_kcnf(n, k)
    
    # Compute Fourier coefficients
    fourier_coeffs = [0] * (1 << n)
    for clause in cnf:
        mask = sum(1 << (abs(v) - 1) for v in clause if v > 0)
        sign = (-1) ** sum(v < 0 for v in clause)
        fourier_coeffs[mask] += sign
    
    max_coeff = max(abs(coeff) for coeff in fourier_coeffs)
    
    # Compute resolution proof length
    proof_length = dpll_solve(cnf)
    
    metric_name = "resolution_proof_length"
    metric_value = proof_length
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    if max_coeff <= 1 / (2 ** (n / 2 - 5)):
        expected_length = 2 ** (n / 2 - 5) * n ** 2
        if abs(proof_length - expected_length) <= 0.1 * expected_length:
            conjecture_holds = True
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]]
    if not seeds:
        seeds = [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_length = sum(r["metric_value"] for r in results) / len(results)
    std_length = math.sqrt(sum((r["metric_value"] - mean_length) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")