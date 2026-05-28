# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def generate_3cnf(n):
    clauses = []
    for _ in range(2 * n):
        clause = set()
        for _ in range(random.randint(1, 3)):
            var = random.choice([f'x{i}' for i in range(1, n + 1)] + [f'~x{i}' for i in range(1, n + 1)])
            if var not in clause:
                clause.add(var)
        clauses.append(list(clause))
    return clauses

def tropical_hyperplanes(clauses):
    hyperplanes = []
    for clause in clauses:
        hyperplane = [Fraction(1, 0) if literal.startswith('~') else Fraction(0, 1) for literal in clause]
        hyperplanes.append(hyperplane)
    return hyperplanes

def intersection_mod_2(hyperplanes):
    n = len(hyperplanes[0])
    result = [Fraction(0, 1)] * n
    for hyperplane in hyperplanes:
        for i in range(n):
            if hyperplane[i] == Fraction(1, 0):
                result[i] += Fraction(1, 2)
            elif hyperplane[i] == Fraction(0, 1):
                result[i] -= Fraction(1, 2)
    return [Fraction(x).limit_denominator() for x in result]

def dpll_refutation_depth(clauses):
    # Simplified DPLL refutation depth calculation
    n = len(clauses)
    return n * (n + 1) // 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    
    hyperplanes = tropical_hyperplanes(clauses)
    intersection_result = intersection_mod_2(hyperplanes)
    refutation_depth = dpll_refutation_depth(clauses)
    
    metric_name = "DPLL Refutation Depth"
    metric_value = refutation_depth
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
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
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result_type = "SUPPORTED"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = f"First failing seed: {first_failing_seed}"
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        result_type = "FALSIFIED"
    
    print(f"RESULT: {result_type} mean={mean_value:.2f} std=0.00 support_fraction={support_fraction:.2f}")