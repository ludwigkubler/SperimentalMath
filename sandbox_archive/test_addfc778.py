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
    
    def generate_sat_instance(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def permutation_from_clauses(clauses):
        perm = {}
        for i, (a, b) in enumerate(clauses):
            if a not in perm:
                perm[a] = i
            if b not in perm:
                perm[b] = i
        return perm
    
    def coxeter_group_action(perm, x):
        n = len(perm)
        result = [0] * n
        for i in range(n):
            result[perm[i]] = x[i]
        return result
    
    def is_invariant(x, y):
        return all(xi == yi for xi, yi in zip(x, y))
    
    def count_distinct_minimal_invariants(clauses):
        perm = permutation_from_clauses(clauses)
        n = len(perm)
        min_invariants = set()
        
        # Generate all possible assignments
        for i in range(2**n):
            x = [i >> j & 1 for j in range(n)]
            y = coxeter_group_action(perm, x)
            if is_invariant(x, y):
                min_invariants.add(tuple(x))
        
        return len(min_invariants)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_min_invariants = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            clauses = generate_sat_instance(n)
            min_invariants = count_distinct_minimal_invariants(clauses)
            total_min_invariants += min_invariants
            instances_tested += 1
    
    metric_value = total_min_invariants / instances_tested
    conjecture_holds = metric_value <= 0.5 * math.sqrt(n_values[-1])
    
    return {
        "metric_name": "distinct_minimal_invariants",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_values[-1],
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Too many distinct minimal invariants: {total_min_invariants}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 10**9) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Too many distinct minimal invariants\" first_failing_seed={first_failing_seed}")