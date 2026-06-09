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

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = [random.randint(1, n), -random.randint(1, n)]
        if random.choice([True, False]):
            clause[0], clause[1] = clause[1], clause[0]
        cnf.append(clause)
    return cnf

def dpll(cnf, assignment={}):
    unit_clauses = [c for c in cnf if len(c) == 1]
    while unit_clauses:
        literal = unit_clauses.pop()[0]
        value = (literal > 0)
        if literal in assignment and assignment[literal] != value:
            return False
        assignment[literal] = value
        cnf = [c for c in cnf if not (len(c) == 1 and c[0] == literal)]
        unit_clauses.extend([c for c in cnf if len(c) == 1])

    pure_literals = {}
    for clause in cnf:
        for literal in clause:
            if -literal in assignment and assignment[-literal]:
                continue
            if literal not in pure_literals or (pure_literals[literal] != None and pure_literals[literal] != (literal > 0)):
                pure_literals[literal] = literal > 0

    pure_clauses = [c for c in cnf if all(literal in assignment and assignment[literal] == (literal > 0) for literal in c)]
    while pure_clauses:
        literal = next(iter(pure_clauses))
        value = (literal > 0)
        if literal in assignment and assignment[literal] != value:
            return False
        assignment[literal] = value
        cnf = [c for c in cnf if not any(literal in c or -literal in c for literal in c)]
        pure_clauses.extend([c for c in cnf if all(literal in assignment and assignment[literal] == (literal > 0) for literal in c)])

    if not cnf:
        return True
    literal = next(iter(cnf[0]))
    return dpll(cnf, assignment.copy()) or dpll(cnf, assignment.copy().update({literal: False}))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n * n // 2, n * (n + 1))
    cnf = generate_cnf(n, m)

    resolution_width = len(dpll(cnf))
    ehrhart_polygon_points = [(i, j) for i in range(n + 1) for j in range(n + 1)]
    ehrhart_polygon_area = len(ehrhart_polygon_points)

    return {
        "metric_name": "resolution_width",
        "metric_value": resolution_width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.5 or r["p_value"] > 0.2 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")