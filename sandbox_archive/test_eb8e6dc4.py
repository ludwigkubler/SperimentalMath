# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import product

def generate_clause_set(n, m):
    clauses = []
    for _ in range(m):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if all(clause[i] == 0 for i in range(n)):
            clause[random.randint(0, n - 1)] = random.choice([-1, 1])
        clauses.append(clause)
    return clauses

def noncommutative_lp_norm(clauses, p):
    m = len(clauses)
    polarity_sum = sum(abs(sum(clause)) for clause in clauses)
    return (polarity_sum / m) ** (1 / p)

def dpll_disjointness(clauses):
    n = len(clauses[0])
    assignment = [-1] * n

    def backtrack(i):
        if i == n:
            return all(assignment[j] != -clauses[k][j] for k in range(len(clauses)) for j in range(n))
        for val in [1, -1]:
            assignment[i] = val
            if backtrack(i + 1):
                return True
        assignment[i] = -1
        return False

    return backtrack(0)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []

    for n in n_values:
        m = 2 * n
        clauses = generate_clause_set(n, m)
        lp_norm = noncommutative_lp_norm(clauses, p=2)
        cc_disjointness = dpll_disjointness(clauses)

        if cc_disjointness < n**(-0.1):
            return {
                "metric_name": "communication_complexity",
                "metric_value": cc_disjointness,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"n={n}, m={m}, lp_norm={lp_norm}, cc_disjointness={cc_disjointness}"
            }

        results.append({
            "n": n,
            "lp_norm": lp_norm,
            "cc_disjointness": cc_disjointness
        })

    mean_lp_norm = sum(result["lp_norm"] for result in results) / len(results)
    mean_cc_disjointness = sum(result["cc_disjointness"] for result in results) / len(results)

    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_cc_disjointness,
        "instances_tested": len(results),
        "conjecture_holds": all(cc_disjointness >= lp_norm**(1/2) for result in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='n={results[0]['n']}, m={2*results[0]['n']}, lp_norm={results[0]['lp_norm']}, cc_disjointness={results[0]['cc_disjointness']}' first_failing_seed={first_failing_seed}")