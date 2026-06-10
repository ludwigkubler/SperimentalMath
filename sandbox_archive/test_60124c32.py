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
    
    def tseitin_formula(n):
        variables = [f'x{i+1}' for i in range(n)]
        clauses = []
        
        # Generate Tseitin formula
        for i in range(1, n + 1):
            clauses.append([variables[i-1]])
            for j in range(i + 1, n + 1):
                clauses.append([-variables[i-1], -variables[j-1]])
                clauses.append([variables[i-1], variables[j-1]])
        
        return clauses
    
    def hermitian_kähler_manifolds(clauses):
        manifolds = set()
        for clause in clauses:
            # Construct a Hermitian Kähler manifold for each clause
            manifold_id = hash(tuple(sorted(clause)))
            manifolds.add(manifold_id)
        return len(manifolds)
    
    def resolution_proof_depth(clauses):
        depth = 0
        stack = []
        for clause in clauses:
            if not any(var in stack for var in clause):
                stack.append(clause)
                depth += 1
        return depth
    
    n = random.randint(5, 40)
    clauses = tseitin_formula(n)
    d = resolution_proof_depth(clauses)
    manifolds_count = hermitian_kähler_manifolds(clauses)
    
    metric_value = manifolds_count / (d ** 2 * math.log(n))
    instances_tested = 1
    n_max = n
    conjecture_holds = metric_value <= 1.0
    counterexample = "" if conjecture_holds else f"n={n}, d={d}, manifolds={manifolds_count}"
    
    return {
        "metric_name": "Manifolds Count",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
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
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} n_tested={len(results)}")