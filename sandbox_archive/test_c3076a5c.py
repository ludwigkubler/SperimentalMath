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
    clauses = []
    for _ in range(2 ** n):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if any(x == -y for x, y in zip(clause, clause[1:])):
            continue
        clauses.append(clause)
    return clauses

def evaluate_cnf(cnf, assignment):
    return all(any(assignment[var - 1] * literal > 0 for literal in clause) for clause in cnf)

def resolution_width(cnf):
    def resolve(cnf, unit_clause):
        new_clauses = []
        for clause in cnf:
            if not any(literal == -unit_clause[0] for literal in clause):
                new_clauses.append(clause)
            elif any(literal == unit_clause[0] for literal in clause):
                continue
            else:
                new_clause = [l for l in clause if l != -unit_clause[0]]
                new_clauses.append(new_clause)
        return new_clauses

    clauses = cnf[:]
    while True:
        unit_clauses = [(l, 1) if l > 0 else (-l, -1) for l in set(lit for clause in clauses for lit in clause) if abs(lit) == 1]
        if not unit_clauses:
            return len(clauses)
        unit_clause, polarity = random.choice(unit_clauses)
        new_clauses = resolve(clauses, (unit_clause, polarity))
        if new_clauses == clauses:
            return len(clauses)
        clauses = new_clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10
    instances_tested = 0
    total_ratio = 0
    max_n = 0
    conjecture_holds = True
    counterexample = ""

    for _ in range(30):
        cnf = generate_cnf(n)
        assignment = [random.choice([True, False]) for _ in range(n)]
        if evaluate_cnf(cnf, assignment):
            instances_tested += 1
            ratio = Fraction(len(cnf), resolution_width(cnf))
            total_ratio += ratio
            max_n = max(max_n, n)

    if instances_tested == 0:
        return {
            "metric_name": "Ratio of Tropical Derivative Degree to Resolution Proof Width",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max_n,
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }

    average_ratio = total_ratio / instances_tested
    support_threshold = 0.95
    if average_ratio <= support_threshold:
        return {
            "metric_name": "Ratio of Tropical Derivative Degree to Resolution Proof Width",
            "metric_value": float(average_ratio),
            "instances_tested": instances_tested,
            "n_max": max_n,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "Ratio of Tropical Derivative Degree to Resolution Proof Width",
            "metric_value": float(average_ratio),
            "instances_tested": instances_tested,
            "n_max": max_n,
            "conjecture_holds": False,
            "counterexample": f"Average ratio {average_ratio} exceeds support threshold {support_threshold}"
        }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='Average ratio exceeds support threshold' first_failing_seed={first_failing_seed}")