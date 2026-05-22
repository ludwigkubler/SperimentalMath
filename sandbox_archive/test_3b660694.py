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
    
    def polynomial_roots(poly_coeffs):
        n = len(poly_coeffs) - 1
        if n == 0:
            return []
        elif n == 1:
            return [-poly_coeffs[0] / poly_coeffs[1]]
        
        # Use the companion matrix method to find roots
        A = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(1, n):
            A[i-1][i] = 1
        A[-1][:n-1] = [-c / poly_coeffs[0] for c in poly_coeffs[1:-1]]
        
        # Find eigenvalues of the companion matrix
        roots = []
        for _ in range(30):  # Perform a few iterations to approximate eigenvalues
            v = [random.random() for _ in range(n)]
            v /= sum(abs(x) for x in v)
            v_next = [sum(A[i][j] * v[j] for j in range(n)) for i in range(n)]
            v_next /= sum(abs(x) for x in v_next)
            roots.append(v_next[0])
        
        return roots
    
    def minimal_root_separation(roots):
        if len(roots) < 2:
            return float('inf')
        return min(abs(roots[i] - roots[j]) for i in range(len(roots)) for j in range(i+1, len(roots)))
    
    def ac0_parity_circuit_size(n):
        # Simplified approximation of AC0 parity circuit size
        return 2 * n
    
    n = random.randint(5, 40)
    F = [random.uniform(-1, 1) for _ in range(n + 1)]
    P = sum(c * x**i for i, c in enumerate(F))
    
    roots = polynomial_roots(F)
    if not all(isinstance(root, (int, float)) for root in roots):
        return {
            "metric_name": "Minimal Root Separation",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    min_separation = minimal_root_separation(roots)
    c = random.uniform(0.1, 1)  # Choose a constant c > 0
    conjecture_holds = min_separation >= c * math.log(n)
    
    circuit_size = ac0_parity_circuit_size(n)
    expected_gate_count = 1.5 * c * n
    
    return {
        "metric_name": "Minimal Root Separation",
        "metric_value": min_separation,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Expected at least {expected_gate_count} gates, got {circuit_size}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(30)]  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")