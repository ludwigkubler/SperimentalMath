# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations, product

def generate_3sat_instance(n: int) -> list:
    clauses = []
    for _ in range(2 * n):
        literals = [random.choice([1, -1]) * (i + 1) for i in random.sample(range(n), 3)]
        clauses.append(literals)
    return clauses

def dpll(sat_formula: list, assignment: dict = {}) -> bool:
    if not sat_formula:
        return True
    literal, rest = sat_formula[0]
    if abs(literal) in assignment:
        new_assignment = assignment.copy()
        new_assignment[abs(literal)] = (assignment[abs(literal)] == 1) ^ (literal < 0)
        return dpll(rest, new_assignment)
    for value in [True, False]:
        new_assignment = assignment.copy()
        new_assignment[abs(literal)] = value
        if dpll([c for c in rest if literal not in c], new_assignment):
            return True
    return False

def resolution_width(sat_formula: list) -> int:
    width = 0
    seen_literals = set()
    while sat_formula:
        clause, rest = sat_formula[0], sat_formula[1:]
        literals = [l for l in clause if abs(l) not in seen_literals]
        seen_literals.update(abs(l) for l in literals)
        new_clauses = []
        for c in rest:
            for l in literals:
                if -l in c:
                    new_clause = list(set(c) ^ {l, -l})
                    new_clauses.append(new_clause)
                    break
            else:
                continue
            break
        sat_formula = new_clauses
        width = max(width, len(seen_literals))
    return width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    sat_formula = generate_3sat_instance(n)
    S_phi = sum(1 for _ in filter(dpll, [sat_formula]))
    L_phi = resolution_width(sat_formula)
    metric_value = S_phi
    conjecture_holds = S_phi >= 2**(n - L_phi)
    counterexample = "" if conjecture_holds else f"S({n})={S_phi}, L({n})={L_phi}"
    return {
        "metric_name": "Integer Point Count",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30*4 + 1, 4))
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")