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

def dpll(sat_formula):
    def solve(assignment):
        if not sat_formula:
            return True
        literal, rest = sat_formula[0]
        pos_literal = abs(literal)
        neg_literal = -pos_literal
        if pos_literal in assignment and assignment[pos_literal] != (literal > 0):
            return False
        if neg_literal in assignment and assignment[neg_literal] != (literal < 0):
            return False
        for var in range(1, max(sat_formula, key=lambda x: abs(x[0]))[0] + 1):
            if var not in assignment:
                if solve(assignment | {var: True}):
                    return True
                if solve(assignment | {var: False}):
                    return True
        return False
    return solve({})

def resolution_width(sat_formula):
    def resolve(clause1, clause2):
        for l1 in clause1:
            for l2 in clause2:
                if abs(l1) == abs(l2) and (l1 > 0) != (l2 > 0):
                    return [x for x in clause1 + clause2 if x != l1 and x != -l2]
        return None

    def simplify(clauses):
        new_clauses = []
        seen = set()
        for clause in clauses:
            if tuple(sorted(clause)) not in seen:
                new_clauses.append(clause)
                seen.add(tuple(sorted(clause)))
        return new_clauses

    clauses = sat_formula[:]
    while True:
        simplified = simplify(clauses)
        if len(simplified) == len(clauses):
            break
        clauses = simplified
    width = 0
    for clause in clauses:
        width = max(width, len(clause))
    return width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    sat_formula = []
    for _ in range(random.randint(n * 2, n * 3)):
        literals = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if all(l not in literals for l in [-1, 1]):
            literals.append(random.choice([-1, 1]))
        sat_formula.append(tuple(sorted(literals)))
    S_phi = sum(1 for _ in filter(dpll, sat_formula))
    L_phi = resolution_width(sat_formula)
    metric_value = S_phi >= 2**(n - L_phi)
    conjecture_holds = metric_value
    counterexample = "" if conjecture_holds else "S(Φ) < 2^(n - L(Φ))"
    return {
        "metric_name": "S(Φ) >= 2^(n - L(Φ))",
        "metric_value": metric_value,
        "instances_tested": len(sat_formula),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"S(Φ) < 2^(n - L(Φ))\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")