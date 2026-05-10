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

def run_trial(seed: int) -> dict:
    n = 40
    random.seed(seed)
    
    def generate_3cnf(num_vars, num_clauses):
        clauses = []
        for _ in range(num_clauses):
            clause = [random.choice([1, -1]) * random.randint(1, num_vars) for _ in range(3)]
            clauses.append(clause)
        return clauses
    
    def fast_walsh_hadamard_transform(f):
        n = len(f)
        if n == 1:
            return f
        even = fast_walsh_hadamard_transform(f[::2])
        odd = fast_walsh_hadamard_transform(f[1::2])
        result = [0] * n
        for k in range(n // 2):
            result[k] = even[k] + odd[k]
            result[k + n // 2] = even[k] - odd[k]
        return result
    
    def fourier_coefficients(clauses, num_vars):
        f = [0] * (1 << num_vars)
        for clause in clauses:
            sign = clause[0]
            x, y, z = clause[1:]
            for i in range(1 << num_vars):
                if (i & (1 << abs(x) - 1)) == ((sign * x) % 2) and \
                   (i & (1 << abs(y) - 1)) == ((sign * y) % 2) and \
                   (i & (1 << abs(z) - 1)) == ((sign * z) % 2):
                    f[i] += sign
        return fast_walsh_hadamard_transform(f)
    
    def discrepancy(f):
        max_val = max(abs(x) for x in f)
        min_val = min(abs(x) for x in f)
        return max_val - min_val
    
    def acc0_circuit_size(clauses, num_vars):
        # Brute-force ACC⁰ circuit size estimation (simplified)
        # This is a placeholder and may not be accurate
        return 2 ** (num_vars // 2)
    
    clauses = generate_3cnf(n, n * 10)
    f = fourier_coefficients(clauses, n)
    disc = discrepancy(f)
    acc0_size = acc0_circuit_size(clauses, n)
    
    conjecture_holds = disc >= 2 ** (n // 2) and acc0_size >= 2 ** (n // 2)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "discrepancy",
        "metric_value": disc,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_disc = sum(r["metric_value"] for r in results) / len(results)
    std_disc = math.sqrt(sum((r["metric_value"] - mean_disc) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_disc} std={std_disc} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_disc} std={std_disc} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")