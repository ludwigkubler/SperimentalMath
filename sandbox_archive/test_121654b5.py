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

def generate_cnf(n):
    clauses = []
    for _ in range(2**n):
        clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
        if all(clause[i] != -clause[j] for j in range(i)):
            clauses.append(clause)
    return clauses

def dpll(cnf, assignment={}):
    if not cnf:
        return True
    literal = next((l for l in range(1, len(cnf[0]) + 1) if l not in assignment and -l not in assignment), None)
    if literal is None:
        return False
    def propagate(lit):
        new_cnf = []
        for clause in cnf:
            if any(abs(l) == abs(lit) for l in clause):
                continue
            if all(abs(l) != abs(lit) for l in clause):
                return False, {}
            new_clause = [l for l in clause if l != -lit]
            new_cnf.append(new_clause)
        return True, {**assignment, lit: True}
    success, assignment = propagate(literal)
    if success:
        result = dpll(new_cnf, assignment)
        if result:
            return result
    assignment[literal] = False
    success, assignment = propagate(-literal)
    if success:
        return dpll(new_cnf, assignment)
    return False

def geometric_entropy(cnf):
    n = len(cnf[0])
    frequency = [0] * (2**n)
    for clause in cnf:
        index = 0
        for literal in clause:
            index |= (1 << abs(literal) - 1)
        frequency[index] += 1
    entropy = 0
    total_clauses = len(cnf)
    for count in frequency:
        if count > 0:
            p = count / total_clauses
            entropy -= p * math.log2(p)
    return entropy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    mge_sum = 0
    path_length_sum = 0
    instances_tested = 0
    n_max = 0

    for n in n_values:
        cnf = generate_cnf(n)
        if not cnf:
            continue
        mge = geometric_entropy(cnf)
        path_length = dpll(cnf)
        if path_length is False:
            path_length = float('inf')
        mge_sum += mge
        path_length_sum += path_length
        instances_tested += len(cnf)
        n_max = max(n_max, n)

    mean_mge = mge_sum / instances_tested
    mean_path_length = path_length_sum / instances_tested

    correlation_coefficient = (instances_tested * sum(m * p for m, p in zip(mge_values, path_length_values)) -
                               sum(mge_values) * sum(path_length_values)) / \
                              math.sqrt((instances_tested * sum(m**2 for m in mge_values) - sum(mge_values)**2) *
                                        (instances_tested * sum(p**2 for p in path_length_values) - sum(path_length_values)**2))

    return {
        "metric_name": "Geometric Entropy vs DPLL Path Length",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **trial_result}}")
        results.append(trial_result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")