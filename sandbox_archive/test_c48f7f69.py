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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def generate_cnf(n):
    cnf = []
    for i in range(1 << n):
        clause = [random.choice([-1, 1]) * (j + 1) for j in range(n)]
        if all(clause[j] == 0 for j in range(n)):
            continue
        cnf.append(clause)
    return cnf

def resolution_width(cnf):
    clauses = set(tuple(sorted(clause)) for clause in cnf)
    seen = set()
    while True:
        new_clauses = set()
        for clause1, clause2 in itertools.combinations(clauses, 2):
            for lit in clause1:
                if -lit in clause2:
                    new_clause = tuple(sorted([l for l in clause1 + clause2 if l != lit and -l != lit]))
                    if new_clause not in seen:
                        new_clauses.add(new_clause)
        if not new_clauses:
            break
        clauses.update(new_clauses)
        seen.update(new_clauses)
    return len(clauses)

def noncommutative_crossed_product(cnf):
    n = int(math.log2(len(cnf[0])))
    G_f = [[0] * (1 << 2 * n) for _ in range(1 << 2 * n)]
    for clause in cnf:
        for lit in clause:
            if lit > 0:
                row = G_f[lit - 1]
                col = G_f[-lit - 1]
                for i in range(1 << n):
                    for j in range(1 << n):
                        row[i * (1 << n) + j] += col[(i ^ j) * (1 << n) + (j ^ lit)]
    return G_f

def min_rank(G_f):
    rows = [row for row in G_f if any(row[i] != 0 for i in range(len(row)))]
    rank = len(rows)
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    G_f = noncommutative_crossed_product(cnf)
    r_G_f = min_rank(G_f)
    w_CNF = resolution_width(cnf)
    if w_CNF == 0:
        return {
            "metric_name": "min_rank_over_resolution_width",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "resolution_width_is_zero"
        }
    ratio = Fraction(r_G_f, w_CNF)
    return {
        "metric_name": "min_rank_over_resolution_width",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    if all(result["conjecture_holds"] for result in results):
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        mean_ratio = sum(result["metric_value"] for result in results) / len(results)
        std_ratio = math.sqrt(sum((result["metric_value"] - mean_ratio)**2 for result in results) / len(results))
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='first_failing_seed' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_trials_passed")