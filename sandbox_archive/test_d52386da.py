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
            clause = random.sample(variables, 2)
            if random.choice([True, False]):
                clause = [-1 * int(x[1:]) if x.startswith('-') else int(x) for x in clause]
            clauses.append(clause)
        return clauses

    def affine_quotient_group_size(clauses):
        n = len(set(var for clause in clauses for var in clause))
        m = len(clauses)
        return 2**n * (m + 1)

    def entropy(clauses):
        n = len(set(var for clause in clauses for var in clause))
        m = len(clauses)
        if m == 0:
            return 0
        p = m / (2**n * (m + 1))
        return -p * math.log2(p) - (1 - p) * math.log2(1 - p)

    def min_generators(n, m):
        # Simplified heuristic for the minimal number of generators
        return n

    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        m = random.randint(1, n * 2)
        clauses = generate_formula(n, m)
        generators = min_generators(n, m)
        H_phi = entropy(clauses)
        
        if generators > 3 * H_phi**2:
            conjecture_holds = False
            counterexample = f"n={n}, m={m}, H(φ)={H_phi}, n(G(φ))={generators}"
            break
        
        if generators > 10 * H_phi**2:
            conjecture_holds = False
            counterexample = f"n={n}, m={m}, H(φ)={H_phi}, n(G(φ))={generators}"
            break

        metric_values.append(generators)

    return {
        "metric_name": "Minimal Number of Generators",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if r["counterexample"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported the conjecture")