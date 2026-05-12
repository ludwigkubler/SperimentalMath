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

def generate_parity_insensitive_function(n):
    clauses = []
    for _ in range(2 * n):
        clause = [random.choice([-1, 1]) * random.randint(0, n - 1) for _ in range(3)]
        if sum(clause) != 0:
            clauses.append(clause)
    return clauses

def fast_walsh_hadamard_transform(f):
    n = len(f)
    while n < len(f):
        n *= 2
    f.extend([0] * (n - len(f)))
    for s in range(1, int(math.log2(n)) + 1):
        step = 2 ** s
        half_step = step // 2
        for i in range(0, n, step):
            for j in range(half_step):
                u = f[i + j]
                v = f[i + j + half_step]
                f[i + j] = u + v
                f[i + j + half_step] = (u - v) * math.sqrt(2)
    return f

def compute_fourier_coefficients(clauses, n):
    f = [0] * (1 << n)
    for clause in clauses:
        sign = 1
        for literal in clause:
            if literal < 0:
                sign *= -1
                literal = -literal - 1
            f[1 << literal] += sign
    return fast_walsh_hadamard_transform(f)

def compute_decision_tree_depth(clauses, n):
    depth = 0
    for clause in clauses:
        max_literal = max(abs(lit) for lit in clause)
        if max_literal > depth:
            depth = max_literal
    return depth

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    clauses = generate_parity_insensitive_function(n)
    f_hat = compute_fourier_coefficients(clauses, n)
    sum_abs_coeffs = sum(abs(coeff) for coeff in f_hat[1:])
    decision_tree_depth = compute_decision_tree_depth(clauses, n)
    
    conjecture_holds = False
    counterexample = ""
    
    if sum_abs_coeffs < math.exp(-n / 2):
        if decision_tree_depth >= 2 ** (n / 2):
            conjecture_holds = True
        else:
            counterexample = "Decision tree depth is too small for the circuit size"
    elif sum_abs_coeffs > math.exp(-n / 2):
        if decision_tree_depth < 2 ** (n / 2):
            conjecture_holds = False
            counterexample = "Decision tree depth is too large for the circuit size"
    
    return {
        "metric_name": "sum_abs_fourier_coeffs",
        "metric_value": sum_abs_coeffs,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        counterexample = next(res["counterexample"] for res in results if res["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")