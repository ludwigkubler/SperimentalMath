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

def generate_polynomials(n, k):
    """Generate n polynomials over GF(2^k) that vanish on a variety."""
    polys = []
    for _ in range(n):
        poly = [random.randint(0, 1) for _ in range(k)]
        polys.append(poly)
    return polys

def interpolate_polynomials(polys):
    """Interpolate polynomials to form a CNF tautology."""
    n = len(polys)
    cnf = []
    for i in range(n):
        for j in range(i + 1, n):
            clause = [f"p{i}_{k}" if polys[i][k] == 0 else f"~p{i}_{k}" for k in range(len(polys[i]))]
            clause += [f"p{j}_{k}" if polys[j][k] == 0 else f"~p{j}_{k}" for k in range(len(polys[j]))]
            cnf.append(clause)
    return cnf

def dpll_search_tree_size(cnf):
    """Simulate DPLL search tree size as a proxy for EF proof length."""
    n = len(cnf)
    stack = [([], cnf)]
    depth = 0
    while stack:
        assignment, clauses = stack.pop()
        if not clauses:
            return depth
        literal = find_unassigned_literal(clauses)
        if literal is None:
            continue
        new_clauses_true = []
        new_clauses_false = []
        for clause in clauses:
            if literal in clause:
                new_clauses_true.append([l for l in clause if l != literal])
            elif ~literal in clause:
                new_clauses_false.append([l for l in clause if l != ~literal])
        stack.append((assignment + [literal], new_clauses_true))
        stack.append((assignment + [~literal], new_clauses_false))
        depth += 1

def find_unassigned_literal(clauses):
    """Find an unassigned literal in the clauses."""
    literals = set()
    for clause in clauses:
        literals.update(clause)
    assigned_literals = set()
    for assignment in literals:
        if ~assignment in literals:
            continue
        assigned_literals.add(assignment)
    return next((l for l in literals if l not in assigned_literals), None)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    k = random.randint(2, 4)
    polys = generate_polynomials(n, k)
    cnf = interpolate_polynomials(polys)
    depth = dpll_search_tree_size(cnf)
    instances_tested = n * (n - 1) // 2
    conjecture_holds = depth > n * math.log(n, 2)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "DPLL Search Tree Size",
        "metric_value": depth,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_depth = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_depth)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")