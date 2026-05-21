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

def generate_random_3cnf(n, alpha):
    clauses = set()
    while len(clauses) < alpha * n:
        clause = []
        for _ in range(3):
            var = random.randint(0, n - 1)
            lit = random.choice([var, -var])
            if (lit, var) not in clause and (-lit, var) not in clause:
                clause.append(lit)
        clauses.add(tuple(sorted(clause)))
    return clauses

def truth_table(truth_assignment):
    n = len(truth_assignment)
    table_size = 2 ** n
    table = [0] * table_size
    for i in range(table_size):
        assignment = [(i >> j) & 1 for j in range(n)]
        table[i] = all(lit == (assignment[var] if lit > 0 else not assignment[-var]) for var, lit in enumerate(truth_assignment))
    return table

def compute_influences(clauses, truth_table):
    n = len(truth_table)
    influences = [0] * n
    for i in range(n):
        flipped_truth_table = [1 - x if (x & (1 << i)) else x for x in truth_table]
        flipped_clauses = {tuple(sorted(c)) for c in clauses if any(flipped_truth_table[var] != lit for var, lit in enumerate(c))}
        influences[i] = len(clauses) - len(flipped_clauses)
    return influences

def dpll(alpha, assignment):
    n = len(assignment)
    remaining_clauses = [c for c in clauses if any(assignment[var] != lit for var, lit in enumerate(c))]
    if not remaining_clauses:
        return 1
    max_inf_var = max(range(n), key=lambda i: influences[i])
    return dpll(alpha - 1, assignment[:max_inf_var] + [0] + assignment[max_inf_var+1:]) + dpll(alpha - 1, assignment[:max_inf_var] + [1] + assignment[max_inf_var+1:])

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([8, 10, 12, 14])
    alpha = random.choice([3.5, 4.0])
    clauses = generate_random_3cnf(n, alpha)
    truth_assignment = [random.choice([-1, 1]) for _ in range(n)]
    table = truth_table(truth_assignment)
    influences = compute_influences(clauses, table)
    I_max = max(influences)
    tau_KKL = dpll(alpha, [0] * n)
    metric_value = math.log2(tau_KKL + 1) - (1 - I_max) * (n - 1) - 5 * math.sqrt(n)
    conjecture_holds = metric_value >= 0
    counterexample = "" if conjecture_holds else f"n={n}, alpha={alpha}, seed={seed}"
    return {
        "metric_name": "log2(tau_KKL + 1)",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(3, 6)]  # Default to first 30 primes if no seeds provided
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['instances_tested']}, alpha={results[0]['metric_name']}, seed={first_failing_seed}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")