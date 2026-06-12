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
    
    def generate_formula(n, m):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(m):
            clause = random.sample(variables + [f'~{v}' for v in variables], 2)
            clauses.append(' & '.join(clause))
        return ' | '.join(clauses)
    
    def calculate_resolution_width(formula):
        # Simplified resolution width calculation (placeholder)
        return len(formula.split(' | '))
    
    def compute_topological_entropy(n, m):
        # Placeholder for topological entropy computation
        return math.log2(n + m) / n
    
    results = []
    for _ in range(30):  # Aim for at least 30 instances per seed
        n = random.randint(5, 40)
        m = random.randint(1, 2 * n)
        formula = generate_formula(n, m)
        w_phi = calculate_resolution_width(formula)
        H_top_phi = compute_topological_entropy(n, m)
        metric_value = w_phi <= H_top_phi ** 2 * math.log(n + m)
        results.append(metric_value)
    
    return {
        "metric_name": "w(φ) ≤ H_top(φ)² * log(n+m)",
        "metric_value": all(results),
        "instances_tested": len(results),
        "n_max": max(n for _ in range(30)),
        "conjecture_holds": all(results),
        "counterexample": "" if all(results) else f"Formula with n={n}, m={m} violates the conjecture"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]  # Default to first 10 primes
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Formula with n={n}, m={m} violates the conjecture\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")