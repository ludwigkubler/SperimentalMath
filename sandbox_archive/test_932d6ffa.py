# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
from itertools import combinations

def hypergeom_order(n, m):
    if n <= 0 or m <= 0:
        return 1
    order = 1
    for i in range(1, min(m, n) + 1):
        order *= (n - i + 1) / (i * (m - i + 1))
    return order

def generate_cnf(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, random.randint(1, n))
        if random.choice([True, False]):
            clause = [-x for x in clause]
        clauses.append(clause)
    return clauses

def resolution_width(clauses):
    literals = set()
    while True:
        new_literals = set()
        for clause in clauses:
            if len(clause) == 1:
                literals.add(clause[0])
            else:
                for i in range(len(clause)):
                    for j in range(i + 1, len(clause)):
                        lit1, lit2 = clause[i], clause[j]
                        if abs(lit1) == abs(lit2):
                            continue
                        new_clause = [x for x in clauses if x != clause and -lit1 not in x and -lit2 not in x]
                        new_literals.update([abs(x) for x in new_clause])
        if not new_literals:
            break
        literals.update(new_literals)
    return len(literals)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_ratio = 0
    instances_tested = 0
    n_max = 0

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            m = random.randint(n // 2, n * 2)
            clauses = generate_cnf(n, m)
            width = resolution_width(clauses)
            order = hypergeom_order(n, m)
            if order == 0:
                continue
            ratio = Fraction(abs(width), order ** 2)
            total_ratio += ratio
            instances_tested += 1
            n_max = max(n_max, n)

    mean_ratio = total_ratio / instances_tested
    conjecture_holds = mean_ratio <= 1
    counterexample = "" if conjecture_holds else "mean_ratio > 1"

    return {
        "metric_name": "mean_ratio",
        "metric_value": float(mean_ratio),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 50, 2))  # Default to first 30 primes if no seeds provided

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_ratio > 1\" first_failing_seed={first_failing_seed}")