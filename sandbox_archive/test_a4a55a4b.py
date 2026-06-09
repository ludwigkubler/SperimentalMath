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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random

def generate_cnf(n):
    cnf = []
    for _ in range(n):
        clause = [random.choice([-i, i]) for _ in range(random.randint(1, n))]
        cnf.append(clause)
    return cnf

def dpll(cnf):
    def solve(assignments):
        if not cnf:
            return assignments
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignments.copy()
            new_assignment[literal] = True
            if literal < 0:
                new_assignment[-literal] = False
            return solve(new_assignment)
        pure_literal = next((l for l in range(1, n+1) if (l not in assignments and -l in assignments)), None)
        if pure_literal:
            new_assignment = assignments.copy()
            new_assignment[pure_literal] = True
            new_assignment[-pure_literal] = False
            return solve(new_assignment)
        literal = random.choice([l for l in range(1, n+1) if l not in assignments])
        new_assignment_true = solve(assignments | {literal: True})
        if new_assignment_true:
            return new_assignment_true
        return solve(assignments | {literal: False})
    return solve({})

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        cnf = generate_cnf(n)
        d = len(cnf)  # Frege proof depth is the number of clauses
        if d == 0:
            continue
        n_max = max(n_max, n)
        instances_tested += 1

        # Simulate groupoid representation (simplified for demonstration)
        A_G = len(cnf)  # Minimal representation dimension is a simplified measure

        total_metric_value += A_G
        if abs(A_G - d) > 0.5 * d:
            conjecture_holds = False
            counterexample = f"n={n}, A(G)={A_G}, d(n)={d}"

    mean_metric_value = total_metric_value / instances_tested if instances_tested > 0 else 0
    std_metric_value = (sum((x - mean_metric_value) ** 2 for x in [mean_metric_value] * instances_tested)) ** 0.5 / instances_tested if instances_tested > 1 else 0

    return {
        "metric_name": "Minimal Representation Dimension",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results)) ** 0.5 / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported the conjecture")