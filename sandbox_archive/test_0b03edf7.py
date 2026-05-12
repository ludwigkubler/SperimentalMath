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

def fast_walsh_hadamard_transform(f):
    n = len(f)
    while n > 1:
        for i in range(n // 2):
            for j in range(i, i + n // 2):
                temp = f[j]
                f[j] += f[j + n // 2]
                f[j + n // 2] = temp - f[j + n // 2]
        n //= 2
    return f

def compute_fourier_coefficients(clauses, n):
    f = [0] * (1 << n)
    for clause in clauses:
        product = 1
        for literal in clause:
            if literal > 0:
                product *= 1 - 2 * f[literal - 1]
            else:
                product *= 1 + 2 * f[-literal - 1]
        f[0] += product
    return [abs(coeff / (1 << n)) for coeff in fast_walsh_hadamard_transform(f)]

def generate_3sat_clauses(n, m):
    clauses = []
    variables = list(range(1, n + 1))
    for _ in range(m):
        clause = random.sample(variables, random.randint(1, n))
        if random.choice([True, False]):
            clause = [-x for x in clause]
        clauses.append(clause)
    return clauses

def compute_decision_tree_depth(circuit):
    depth = 0
    queue = [circuit]
    while queue:
        next_level = []
        for node in queue:
            if isinstance(node, list):
                next_level.extend(node)
        queue = next_level
        depth += 1
    return depth

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = 2 * n
    clauses = generate_3sat_clauses(n, m)
    f_hat = compute_fourier_coefficients(clauses, n)
    sum_abs_fourier_coeffs = sum(f_hat[1:])
    
    # Simulate AC⁰ circuit size (simplified model)
    ac0_circuit_size = 2 ** (n // 2)
    
    decision_tree_depth = compute_decision_tree_depth(circuit)
    if decision_tree_depth > ac0_circuit_size:
        return {
            "metric_name": "sum_abs_fourier_coeffs",
            "metric_value": sum_abs_fourier_coeffs,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Decision tree depth is too large for the circuit size"
        }
    
    return {
        "metric_name": "sum_abs_fourier_coeffs",
        "metric_value": sum_abs_fourier_coeffs,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Decision tree depth exceeds circuit size\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")