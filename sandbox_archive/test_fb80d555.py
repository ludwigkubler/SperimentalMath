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
from fractions import Fraction
from math import log, log2

def generate_cnf(n):
    cnf = []
    for _ in range(10 * n):  # Generate 10 clauses per variable on average
        clause = [random.randint(-n, -1) if random.choice([True, False]) else random.randint(1, n)
                   for _ in range(random.randint(1, n))]
        cnf.append(clause)
    return cnf

def truth_table(cnf):
    n = len(cnf[0])
    table = []
    for assignment in product([-1, 1], repeat=n):
        table.append(sum([lit if val > 0 else -lit for lit, val in zip(range(1, n+1), assignment)]))
    return table

def min_order(cnf):
    n = len(cnf[0])
    table = truth_table(cnf)
    degree = 1
    while True:
        all_zero = all(table[i] == 0 for i in range(degree) if i < len(table))
        if all_zero:
            return degree
        degree += 1

def frege_proof_length(cnf):
    # Simplified DPLL solver to estimate proof length
    n = len(cnf[0])
    stack = []
    assignment = [None] * (n + 1)
    def dpll():
        if not cnf:
            return 1
        for clause in cnf:
            unit_clause = next((lit for lit in clause if abs(lit) == 1), None)
            if unit_clause:
                literal = unit_clause
                assignment[abs(literal)] = literal > 0
                stack.append(literal)
                res = dpll()
                if res:
                    return res
                stack.pop()
                assignment[abs(literal)] = None
        for i in range(1, n + 1):
            if assignment[i] is None:
                assignment[i] = True
                stack.append(i)
                res = dpll()
                if res:
                    return res
                stack.pop()
                assignment[i] = False
                stack.append(-i)
                res = dpll()
                if res:
                    return res
                stack.pop()
        return 0
    return dpll()

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        cnf = generate_cnf(n)
        min_order_value = min_order(cnf)
        proof_length = frege_proof_length(cnf)
        results.append({"n": n, "min_order": min_order_value, "proof_length": proof_length})
    
    n_max = max(result["n"] for result in results)
    if n_max < 16:
        return {
            "metric_name": "f(n)",
            "metric_value": sum(result["proof_length"] for result in results) / len(results),
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max < 16"
        }
    
    f_n_values = [n ** (log(n) / log(log(n))) for n in n_values]
    correlation_coefficient = pearson_correlation(results, f_n_values)
    return {
        "metric_name": "f(n)",
        "metric_value": sum(result["proof_length"] for result in results) / len(results),
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": ""
    }

def pearson_correlation(data, f_n_values):
    x_mean = sum(result["min_order"] for result in data) / len(data)
    y_mean = sum(f_n_values) / len(f_n_values)
    numerator = sum((result["min_order"] - x_mean) * (f_n_values[i] - y_mean) for i, result in enumerate(data))
    denominator = sum((result["min_order"] - x_mean) ** 2 for result in data) * sum((f_n_values[i] - y_mean) ** 2 for i, _ in enumerate(data)) ** 0.5
    return numerator / denominator if denominator != 0 else 0

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1, 10000) for _ in range(30)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=... support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")