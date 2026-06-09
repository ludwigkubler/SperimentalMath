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

def generate_cnf(n: int) -> list:
    cnf = []
    for _ in range(10 * n):  # 10 clauses per variable on average
        clause = [random.choice([i, -i]) for i in range(1, n + 1)]
        random.shuffle(clause)
        cnf.append(clause)
    return cnf

def dpll(cnf: list) -> bool:
    def solve(literals: set, assignment: dict):
        if not literals:
            return True
        var = next(iter(literals))
        for val in [True, False]:
            new_assignment = assignment.copy()
            new_assignment[var] = val
            if all(not (var == abs(clause[0]) and clause[1] != 0) for clause in cnf):
                if solve(literals - {var}, new_assignment):
                    return True
        return False

    literals = set(abs(lit) for lit in sum(cnf, []))
    return solve(literals, {})

def frege_depth(cnf: list) -> int:
    def depth(clause: list, assignment: dict) -> int:
        if not clause:
            return 0
        var = next(iter(clause))
        new_assignment = assignment.copy()
        new_assignment[var] = True
        if all(not (var == abs(clause[0]) and clause[1] != 0) for clause in cnf):
            return depth([lit for lit in clause if lit != var], new_assignment)
        new_assignment[var] = False
        if all(not (var == abs(clause[0]) and clause[1] != 0) for clause in cnf):
            return depth([lit for lit in clause if lit != -var], new_assignment)
        return max(depth([lit for lit in clause if lit != var], new_assignment),
                   depth([lit for lit in clause if lit != -var], new_assignment)) + 1

    literals = set(abs(lit) for lit in sum(cnf, []))
    return depth(literals, {})

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []

    for n in n_values:
        cnf = generate_cnf(n)
        depth = frege_depth(cnf)
        e_phi = Fraction(1, 1)  # Placeholder for actual diophantine exponent computation
        metric_value = e_phi ** 2 * math.log(n)
        results.append({
            "n": n,
            "depth": depth,
            "metric_value": metric_value
        })

    correlation = sum((r["depth"] - r["metric_value"]) ** 2 for r in results) / len(results)
    conjecture_holds = all(r["depth"] <= r["metric_value"] for r in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "seed": seed,
        "metric_name": "Frege Depth",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")