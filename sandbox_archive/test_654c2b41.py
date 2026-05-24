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

def generate_cnf(n):
    cnf = []
    for i in range(1 << n):
        clause = [random.choice([-1, 1]) * (j + 1) for j in range(n)]
        if all(clause[j] != -clause[(j + 1) % n] for j in range(n)):
            cnf.append(clause)
    return cnf

def resolution_width(cnf):
    clauses = set(tuple(sorted(clause)) for clause in cnf)
    queue = list(clauses)
    while queue:
        clause1, clause2 = queue.pop()
        for lit in clause1:
            if -lit in clause2:
                new_clause = tuple(sorted(set(clause1) | set(clause2) - {lit, -lit}))
                if len(new_clause) == 1:
                    return len(queue)
                if new_clause not in clauses:
                    queue.append(new_clause)
                    clauses.add(new_clause)
    return float('inf')

def noncommutative_crossed_product(cnf):
    n = int(cnf[0][0].bit_length() - 1)
    G_f = [[0] * (2 ** (n + 1)) for _ in range(2 ** (n + 1))]
    for clause in cnf:
        for lit in clause:
            i, j = divmod(abs(lit) - 1, n)
            sign = -1 if lit < 0 else 1
            for k in range(n):
                G_f[i * (1 << n) + j][k * (1 << n) + (j ^ lit)] += sign
    return G_f

def min_rank(G_f):
    rows, cols = len(G_f), len(G_f[0])
    rank = 0
    for i in range(rows):
        if any(G_f[i][j] != 0 for j in range(cols)):
            rank += 1
            for j in range(cols):
                if G_f[i][j] != 0:
                    for k in range(rows):
                        G_f[k][j] -= (G_f[k][i] * G_f[i][j]) / G_f[i][i]
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    r_G_f = min_rank(noncommutative_crossed_product(cnf))
    w_CNF_f = resolution_width(cnf)
    if w_CNF_f == float('inf'):
        return {
            "metric_name": "min_rank_over_resolution_width",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "resolution_width_infinite"
        }
    c = 2  # Example constant, adjust as needed
    conjecture_holds = r_G_f <= c * w_CNF_f
    return {
        "metric_name": "min_rank_over_resolution_width",
        "metric_value": r_G_f / w_CNF_f,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"c={c}, r(G_f)={r_G_f}, w(CNF(f))={w_CNF_f}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **trial_result}}")
        results.append(trial_result)

    if all("conjecture_holds" not in result or result["conjecture_holds"] for result in results):
        support_fraction = sum(1 for result in results if "conjecture_holds" in result and result["conjecture_holds"]) / len(results)
        RESULT = f"SUPPORTED mean={sum(result['metric_value'] for result in results) / len(results)} std=0.0 support_fraction={support_fraction}"
    elif any("counterexample" in result for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "conjecture_holds" not in result or not result["conjecture_holds"])
        RESULT = f"FALSIFIED counterexample=\"{next(result['counterexample'] for result in results if 'counterexample' in result)}\" first_failing_seed={first_failing_seed}"
    else:
        RESULT = "INCONCLUSIVE no_data"

    print(RESULT)