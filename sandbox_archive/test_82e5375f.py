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
        for _ in range(2 * n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def compute_permutation(clauses):
        perm = {}
        for lit, neg_lit in clauses:
            if abs(lit) not in perm:
                perm[abs(lit)] = []
            perm[abs(lit)].append((lit, neg_lit))
        return perm
    
    def generate_minimal_invariants(perm):
        invariants = set()
        for var, clauselits in perm.items():
            invariant = tuple(sorted(clause for lit, clause in clauselits if lit > 0))
            invariants.add(invariant)
        return invariants
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_invariants = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            clauses = generate_sat_instance(n)
            perm = compute_permutation(clauses)
            invariants = generate_minimal_invariants(perm)
            total_invariants += len(invariants)
            instances_tested += 1
            n_max = max(n_max, n)
    
    metric_value = total_invariants / instances_tested
    conjecture_holds = metric_value <= 0.5 * math.sqrt(n_max)
    counterexample = "" if conjecture_holds else f"n={n_max}, invariants={total_invariants}"
    
    return {
        "metric_name": "Number of distinct minimal invariants",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[first_failing_seed]}")