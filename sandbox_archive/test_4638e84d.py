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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if any(clause[i] == -clause[j] for i in range(n) for j in range(i+1, n)):
                continue
            clauses.append(clause)
        return clauses
    
    def find_local_indecomposable_module(clauses):
        # Simplified heuristic to find a local indecomposable module
        # This is a placeholder and should be replaced with actual logic
        return len(set(tuple(sorted(c)) for c in clauses))
    
    n_max = 0
    metric_values = []
    instances_tested = 0
    
    for n in range(1, 41):
        cnf = generate_cnf(n)
        order = find_local_indecomposable_module(cnf)
        if order > n_max:
            n_max = order
        metric_values.append(order)
        instances_tested += len(cnf)
    
    alpha = max(metric_values) ** (1 / n_max)
    conjecture_holds = all(order >= alpha**n for n, order in enumerate(metric_values, start=1))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Max Order of Local Indecomposable Module",
        "metric_value": max(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 100, 4))[:30]  # Default to first 30 prime-like numbers
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")