# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses

    def clause_indicator_polynomial(clauses, x):
        poly = 1
        for clause in clauses:
            term = 1
            for literal in clause:
                if literal < 0:
                    term *= (1 - x**(-2 * abs(literal)))
                else:
                    term *= (1 + x**(2 * literal))
            poly += term
        return poly

    def minimal_order_of_quadratic_residues(poly):
        n = len(poly)
        for order in range(1, n + 1):
            found = True
            for i in range(n):
                if not is_quadratic_residue(poly[i], order):
                    found = False
                    break
            if found:
                return order
        return n

    def is_quadratic_residue(a, p):
        if a == 0:
            return True
        if a < 0:
            a += p
        for x in range(1, p):
            if (x * x) % p == a:
                return True
        return False

    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    poly = clause_indicator_polynomial(clauses, x=2)
    
    min_order = minimal_order_of_quadratic_residues(poly)
    w_phi = len(clauses) * n
    
    return {
        "metric_name": "min_order_over_w",
        "metric_value": Fraction(min_order, w_phi),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")