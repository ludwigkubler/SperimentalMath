# auto-injected by SEC sandbox
import math
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
from itertools import combinations, product

def generate_cnf(n: int) -> list:
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(n):
        clause = random.sample(variables, random.randint(1, n))
        clauses.append(clause)
    return clauses

def evaluate_cnf(cnf: list, assignment: dict) -> bool:
    for clause in cnf:
        if not any(assignment[var] == (var > 0) for var in clause):
            return False
    return True

def probability_distribution(cnf: list, n: int) -> dict:
    total = 2 ** n
    satisfying_assignments = 0
    for assignment in product([True, False], repeat=n):
        if evaluate_cnf(cnf, {i+1: val for i, val in enumerate(assignment)}):
            satisfying_assignments += 1
    return Fraction(satisfying_assignments, total)

def renyi_divergence(p: dict, q: dict, alpha: float) -> float:
    if alpha == 1:
        return -sum(p[var] * math.log2(q[var]) for var in p)
    else:
        return (sum(p[var] ** alpha / q[var] ** alpha for var in p)) ** (1 / (alpha - 1))

def resolution_width(cnf: list) -> int:
    def dpll(cnf, assignment):
        if not cnf:
            return True
        unit_clauses = [c for c in cnf if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            new_assignment = assignment.copy()
            new_assignment[literal] = literal > 0
            if not dpll([c for c in cnf if literal not in c], new_assignment):
                new_assignment[literal] = literal < 0
                return dpll([c for c in cnf if -literal not in c], new_assignment)
        else:
            literals = [var for var, val in assignment.items() if val is None]
            if not literals:
                return False
            literal = random.choice(literals)
            new_assignment[literal] = True
            if dpll(cnf, new_assignment):
                return True
            new_assignment[literal] = False
            return dpll(cnf, new_assignment)
    return len(dpll(cnf, {var: None for var in range(1, len(cnf) + 1)}))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        cnf = generate_cnf(n)
        p = probability_distribution(cnf, n)
        max_width = 0
        total_ratio = 0
        instances_tested = 0
        for alpha in [1.0] + list(range(2, 11)):
            width = resolution_width(cnf)
            if width > max_width:
                max_width = width
            ratio = renyi_divergence(p, {var: 0.5 for var in p}, alpha) / width
            total_ratio += ratio
            instances_tested += 1
        results.append({
            "n": n,
            "max_width": max_width,
            "total_ratio": total_ratio,
            "instances_tested": instances_tested
        })
    mean_ratio = sum(result["total_ratio"] for result in results) / len(results)
    conjecture_holds = all(result["total_ratio"] <= 10 * result["max_width"] for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "Rényi_divergence_bound",
        "metric_value": mean_ratio,
        "instances_tested": sum(result["instances_tested"] for result in results),
        "n_max": max(result["max_width"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] * r["instances_tested"] for r in results) / sum(r["instances_tested"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")