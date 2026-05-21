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

def generate_3cnf(n, alpha):
    clauses = []
    for _ in range(int(alpha * n)):
        clause = [random.choice([-1, 1]) * (i + 1) for i in random.sample(range(n), 3)]
        clauses.append(clause)
    return clauses

def truth_table(f, n):
    table = {}
    for i in range(2**n):
        assignment = [(i >> j) & 1 for j in range(n)]
        table[tuple(assignment)] = f(assignment)
    return table

def influence(f, n):
    inf = [0] * n
    for var in range(n):
        flips = {tuple(assignment[:var] + [1-assignment[var]] + assignment[var+1:]) for assignment in truth_table(f, n).keys()}
        inf[var] = sum(truth_table(f, n)[flip] != f(list(flip)) for flip in flips) / (2**n)
    return inf

def dpll(alpha, assignment):
    if not any(clause for clause in alpha):
        return 1
    var = min(range(len(assignment)), key=lambda v: sum(1 for c in alpha if any(assignment[var] != lit for var, lit in enumerate(c))))
    left_assignment = assignment[:]
    right_assignment = assignment[:]
    left_assignment[var] = 0
    right_assignment[var] = 1
    return dpll(alpha_new(left_assignment), left_assignment) + dpll(alpha_new(right_assignment), right_assignment)

def alpha_new(assignment):
    return [c for c in alpha if any(assignment[var] != lit for var, lit in enumerate(c))]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([8, 10, 12, 14])
    alpha = generate_3cnf(n, random.uniform(3.5, 4.0))
    f_F = lambda x: all(c for c in alpha if any(x[var] != lit for var, lit in enumerate(c)))
    table = truth_table(f_F, n)
    inf = influence(f_F, n)
    I_max = max(inf)
    tau_KKL = dpll(alpha, [0] * n)
    metric_value = math.log2(tau_KKL + 1)
    conjecture_holds = metric_value <= (1 - I_max) * (n - 1) + 5 * math.sqrt(n)
    counterexample = "" if conjecture_holds else f"tau_KKL={tau_KKL}, I_max={I_max}"
    return {
        "metric_name": "log2(tau_KKL + 1)",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric = sum(r["metric_value"] for r in results) / len(results)
    std_metric = math.sqrt(sum((r["metric_value"] - mean_metric)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")