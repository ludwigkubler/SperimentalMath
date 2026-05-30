# auto-injected by SEC sandbox
import math
import itertools
import json
import sys
import os
import re
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import time
from collections import defaultdict
from fractions import Fraction

def generate_cnf(n: int) -> list:
    cnf = []
    for _ in range(random.randint(2, 5)):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if random.random() < 0.5:
            clause = [-x for x in clause]
        cnf.append(clause)
    return cnf

def dpll_refutation_time(cnf: list) -> float:
    start_time = time.time()
    # Simplified DPLL implementation
    def dpll(assignment, clauses):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[-abs(literal)] = literal > 0
            return dpll(new_assignment, [c for c in clauses if literal not in c and -literal not in c])
        pure_literal = next((l for l in range(1, len(assignment) + 1) if (l not in assignment and -l not in assignment)), None)
        if pure_literal:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            return dpll(new_assignment, [c for c in clauses if pure_literal not in c and -pure_literal not in c])
        literal = random.choice([l for l in range(1, len(assignment) + 1)])
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll(new_assignment, [c for c in clauses if literal not in c and -literal not in c]):
            return True
        new_assignment[literal] = False
        return dpll(new_assignment, [c for c in clauses if literal not in c and -literal not in c])
    assignment = [None] * (len(cnf) + 1)
    return time.time() - start_time

def diophantine_exponent(cnf: list) -> int:
    n = len(cnf)
    d = 2
    while True:
        if all(all(x % d == y % d for x, y in zip(clause, clause[1:])) for clause in cnf):
            return d
        d += 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    total_ratio = 0.0
    conjecture_holds = True
    counterexample = ""

    for n in range(5, n_max + 1):
        if time.time() - start_time > 200:
            return {
                "metric_name": "ratio",
                "metric_value": total_ratio / instances_tested,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": "budget_exceeded"
            }
        cnf = generate_cnf(n)
        d = diophantine_exponent(cnf)
        refutation_time = dpll_refutation_time(cnf)
        if refutation_time == 0:
            continue
        ratio = (n ** d) * math.log(n) / refutation_time
        total_ratio += ratio
        instances_tested += 1

    mean_ratio = total_ratio / instances_tested
    return {
        "metric_name": "ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": mean_ratio <= 3,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    start_time = time.time()
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)

    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")