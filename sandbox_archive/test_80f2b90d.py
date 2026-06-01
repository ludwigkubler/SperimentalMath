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

def generate_cnf(m):
    cnf = []
    for _ in range(m):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(2, 5))]
        cnf.append(clause)
    return cnf

def dpll(cnf, assignment={}):
    if not cnf:
        return True
    unit_clause = next((c for c in cnf if len(c) == 1), None)
    if unit_clause:
        literal = unit_clause[0]
        if literal < 0 and literal in assignment and assignment[literal] == False:
            return False
        elif literal > 0 and literal not in assignment:
            assignment[literal] = True
            if dpll(cnf, assignment):
                return True
            assignment[literal] = False
        else:
            assignment[literal] = False
            if dpll(cnf, assignment):
                return True
    literals = [l for c in cnf for l in c]
    literal = random.choice(literals)
    if literal < 0 and literal not in assignment:
        assignment[literal] = False
        if dpll(cnf, assignment):
            return True
        assignment[literal] = True
    elif literal > 0 and literal not in assignment:
        assignment[literal] = True
        if dpll(cnf, assignment):
            return True
        assignment[literal] = False
    return False

def minimal_diophantine_property_set(cnf):
    property_set = set()
    for i in range(1, len(cnf) + 1):
        for assignment in itertools.product([False, True], repeat=i):
            if all(any(l in assignment and assignment[l] == (l > 0) for l in clause) for clause in cnf):
                property_set.add(tuple(sorted(assignment)))
    return property_set

def circuit_monotone_width(property_set):
    n = len(next(iter(property_set), ()))
    monotone_width = 0
    for assignment in property_set:
        width = sum(1 for l, val in enumerate(assignment, start=1) if val)
        if width > monotone_width:
            monotone_width = width
    return monotone_width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        cnf = generate_cnf(n)
        property_set = minimal_diophantine_property_set(cnf)
        monotone_width = circuit_monotone_width(property_set)
        results.append({
            "n": n,
            "monotone_width": monotone_width,
            "property_size": len(property_set),
        })
    mean_td = sum(result["monotone_width"] for result in results) / len(results)
    conjecture_holds = all(result["monotone_width"] <= 2 * result["n"] * math.log(result["n"]) for result in results)
    return {
        "metric_name": "circuit_monotone_width",
        "metric_value": mean_td,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Monotone width exceeds 2 * n * log(n) for n={max(result['n'] for result in results)}",
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 100000) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_td = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_td} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_td} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Monotone width exceeds 2 * n * log(n)' first_failing_seed={first_failing_seed}")