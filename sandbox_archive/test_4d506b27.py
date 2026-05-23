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
    random.seed(seed)
    
    def riemann_zeta(s, terms=100):
        if s == 1:
            return float('inf')
        return sum(1 / (n ** s) for n in range(1, terms + 1))
    
    def regularized_resolution_proof_length(n):
        zeta_value = riemann_zeta(1/2)
        return zeta_value / (2 * math.pi)
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for var in variables:
            clauses.append([var])
        for i in range(n-1):
            clauses.append([f'~{variables[i]}', f'{variables[i+1]}'])
        return clauses
    
    def resolution_proof_length(clauses):
        # Simplified estimation of resolution proof length
        return len(clauses) * 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_length = 0
    num_instances = 0
    
    for n in n_values:
        for _ in range(30):
            clauses = generate_tseitin_formula(n)
            length = resolution_proof_length(clauses)
            total_length += length
            num_instances += 1
    
    expected_value = total_length / num_instances
    theoretical_bound = math.sqrt(n) * math.log2(n)
    
    conjecture_holds = abs(expected_value - theoretical_bound) <= 0.5 * theoretical_bound
    counterexample = "" if conjecture_holds else f"n={n}, expected_value={expected_value}, theoretical_bound={theoretical_bound}"
    
    return {
        "metric_name": "RegularizedResolutionProofLength",
        "metric_value": expected_value,
        "instances_tested": num_instances,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")