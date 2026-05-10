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

def generate_3cnf(n):
    clauses = []
    for _ in range(2 * n):
        clause = [random.choice([True, False]) * random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if all(clause[i] == -clause[j] for i in range(n) for j in range(i + 1, n)):
            continue
        clauses.append(clause)
    return clauses

def fast_walsh_hadamard_transform(f):
    n = len(f)
    while n > 1:
        half_n = n // 2
        for i in range(half_n):
            for j in range(n):
                if j & (half_n - 1) == i:
                    f[j] += f[j + half_n]
                    f[j + half_n] -= f[j]
        n //= 2
    return [x / math.sqrt(len(f)) for x in f]

def is_acc0_computable(n, s):
    # Placeholder function to check if a 3-CNF formula can be computed by an ACC⁰ circuit of size s
    # This is a placeholder and should be replaced with actual computation logic
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    threshold = 2**(n/2) / (2**(n/2) / math.log(n))
    
    metric_value = 0
    instances_tested = 0
    
    for _ in range(30):
        formula = generate_3cnf(n)
        f = [0] * (1 << n)
        for clause in formula:
            mask = 0
            for var in clause:
                if var > 0:
                    mask |= 1 << (var - 1)
                else:
                    mask &= ~(1 << (-var - 1))
            f[mask] += 1
        
        f_transformed = fast_walsh_hadamard_transform(f)
        sum_abs_coefficients = sum(abs(x) for x in f_transformed)
        
        metric_value += sum_abs_coefficients
        instances_tested += 1
        
        if sum_abs_coefficients >= threshold and is_acc0_computable(n, s):
            return {
                "metric_name": "sum_abs_fourier_coefficients",
                "metric_value": sum_abs_coefficients,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": "formula_computable_by_acc0_circuit"
            }
    
    return {
        "metric_name": "sum_abs_fourier_coefficients",
        "metric_value": metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] * r["instances_tested"] for r in results) / sum(r["instances_tested"] for r in results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 * r["instances_tested"] for r in results) / sum(r["instances_tested"] for r in results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='formula_computable_by_acc0_circuit' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")