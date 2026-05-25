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

def generate_random_3cnf(n):
    clauses = []
    for _ in range(10 * n):  # Each variable appears in about 10 clauses
        clause = [random.choice([1, -1]) * (i + 1) for i in random.sample(range(n), 3)]
        clauses.append(clause)
    return clauses

def dpll(clauses):
    def solve(model):
        if not clauses:
            return model
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            if literal < 0 and -literal in model:
                return None
            new_model = model.copy()
            new_model[literal] = True
            return solve([c for c in clauses if literal not in c and -literal not in c])
        pure_literal = next((l for l in range(1, n + 1) if (l not in model and any(l in c for c in clauses)) or (-l not in model and any(-l in c for c in clauses))), None)
        if pure_literal:
            new_model = model.copy()
            new_model[pure_literal] = True
            return solve([c for c in clauses if pure_literal not in c and -pure_literal not in c])
        literal = random.choice([1, -1]) * (random.randint(1, n))
        new_model = model.copy()
        new_model[literal] = True
        result = solve([c for c in clauses if literal not in c and -literal not in c])
        if result is None:
            new_model[literal] = False
            return solve([c for c in clauses if literal not in c and -literal not in c])
        return result
    model = {}
    return solve(model)

def tropicalized_hodge_diamond(clauses):
    n = len(clauses[0]) // 3
    hodge_diamond = [[0] * (n + 1) for _ in range(n + 1)]
    for clause in clauses:
        for literal in clause:
            if literal > 0:
                hodge_diamond[literal - 1][0] += 1
            else:
                hodge_diamond[-literal - 1][0] -= 1
    return hodge_diamond

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    clauses = generate_random_3cnf(n)
    resolution_length = dpll(clauses)
    if resolution_length is None:
        resolution_length = float('inf')
    hodge_diamond = tropicalized_hodge_diamond(clauses)
    H_n_G = sum(sum(row) for row in hodge_diamond)
    c = 10  # Example constant, can be adjusted
    log_cubed_n = c * (n ** 3).bit_length()
    metric_value = resolution_length
    conjecture_holds = resolution_length <= 2 ** (O(H_n_G))
    counterexample = "" if conjecture_holds else f"H_n(G)={H_n_G}, resolution_length={resolution_length}"
    return {
        "metric_name": "Resolution Proof Length",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
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

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")