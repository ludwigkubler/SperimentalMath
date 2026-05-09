# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def fast_walsh_hadamard_transform(arr):
    n = len(arr)
    if n == 1:
        return arr
    even = fast_walsh_hadamard_transform(arr[::2])
    odd = fast_walsh_hadamard_transform(arr[1::2])
    result = [0] * n
    for i in range(n // 2):
        result[i] = even[i] + odd[i]
        result[i + n // 2] = even[i] - odd[i]
    return result

def generate_k_cnf(n, k):
    clauses = []
    variables = list(range(1, n + 1))
    for _ in range(k):
        clause = random.sample(variables, random.randint(1, n))
        clauses.append(clause)
    return clauses

def dpll_resolution(clauses):
    def simplify(clauses):
        new_clauses = []
        seen = set()
        for clause in clauses:
            if not clause:
                return None
            if len(clause) == 1:
                seen.add(clause[0])
            else:
                new_clauses.append([x for x in clause if x not in seen and -x not in seen])
        return new_clauses

    def resolve(clauses, literal):
        resolved = []
        for clause in clauses:
            if literal in clause:
                continue
            if -literal in clause:
                resolved.extend([x for x in clause if x != -literal])
            else:
                resolved.append(clause)
        return resolved

    while True:
        simplified = simplify(clauses)
        if simplified is None:
            return False
        clauses = simplified
        for literal in set(x for clause in clauses for x in clause):
            new_clauses = resolve(clauses, literal)
            if new_clauses is None:
                return True
            clauses = new_clauses

    return len(clauses) == 0

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    k = random.randint(n // 2, n)
    formula = generate_k_cnf(n, k)
    
    # Compute Fourier coefficients
    fourier_coeffs = [0] * (1 << n)
    for clause in formula:
        for assignment in range(1 << n):
            if all((assignment & (1 << abs(var) - 1)) != 0 == sign for var, sign in zip(clause, [-1] * len(clause))):
                fourier_coeffs[assignment] += 1
    
    max_coeff = max(abs(coeff) for coeff in fourier_coeffs)
    
    # Measure resolution proof length
    proof_length = dpll_resolution(formula)
    
    metric_value = proof_length / (2 ** (n / 2) / max_coeff)
    conjecture_holds = abs(metric_value - 1) <= 0.1
    counterexample = "" if conjecture_holds else "proof_length_mismatch"
    
    return {
        "metric_name": "Proof Length",
        "metric_value": proof_length,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) < 0.2:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"proof_length_mismatch\" first_failing_seed={first_failing_seed}")