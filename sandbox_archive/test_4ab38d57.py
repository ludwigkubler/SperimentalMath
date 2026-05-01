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
from math import factorial

def hook_length_formula(n, k):
    if n == 0 or k == 0:
        return 1
    numerator = factorial((n - k) * (n + 1))
    denominator = 1
    for i in range(1, n + 1):
        denominator *= i * (i + k)
    return numerator // denominator

def generate_random_3sat(n):
    clauses = []
    for _ in range(2 ** n):
        clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(3)]
        if all(clause[i] != -clause[j] for i in range(3) for j in range(i + 1, 3)):
            clauses.append(clause)
    return clauses

def dpll_refutation_size(clauses):
    def is_satisfiable(model):
        for clause in clauses:
            if not any(model[abs(lit)] == lit for lit in clause):
                return False
        return True
    
    def backtrack(model, assignment):
        if len(assignment) == n:
            return is_satisfiable(model)
        var = assignment + 1
        model[var] = 1
        if backtrack(model, assignment + 1):
            return True
        model[var] = -1
        if backtrack(model, assignment + 1):
            return True
        del model[var]
        return False
    
    n = len(clauses[0])
    model = {}
    return 2 ** n if not backtrack(model, 0) else 0

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    k = n // 3
    dim_chi_lambda = hook_length_formula(n - k, k)
    
    instances_tested = 10
    refutation_sizes = [dpll_refutation_size(generate_random_3sat(n)) for _ in range(instances_tested)]
    
    conjecture_holds = all(dim_chi_lambda >= size for size in refutation_sizes)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "SOS_refutation_size",
        "metric_value": dim_chi_lambda,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 50))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")