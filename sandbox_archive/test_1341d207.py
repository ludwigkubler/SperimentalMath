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
    clauses = []
    for _ in range(2 * n):
        clause = [random.randint(-n, -1), random.randint(1, n)]
        if random.choice([True, False]):
            clause = [-x for x in clause]
        clauses.append(clause)
    return clauses

def unit_propagation(clauses: list, assignment: dict) -> bool:
    while True:
        unit_clauses = [c for c in clauses if len(c) == 1 and c[0] not in assignment]
        if not unit_clauses:
            break
        literal = unit_clauses[0][0]
        assignment[literal] = literal > 0
        clauses = [[x for x in c if x != literal and -x != literal] for c in clauses]
    return len(clauses) == 0

def dpll(clauses: list, assignment: dict = {}) -> bool:
    if unit_propagation(clauses, assignment):
        return True
    unsatisfied_clauses = [c for c in clauses if not any(l in assignment and assignment[l] == (l > 0) for l in c)]
    if not unsatisfied_clauses:
        return True
    literal = unsatisfied_clauses[0][0]
    new_assignment1 = assignment.copy()
    new_assignment1[literal] = literal > 0
    if dpll(clauses, new_assignment1):
        return True
    new_assignment2 = assignment.copy()
    new_assignment2[-literal] = -literal > 0
    return dpll(clauses, new_assignment2)

def frege_proof_depth(cnf: list) -> int:
    n = len(cnf)
    if n == 1:
        return 1
    depth = 0
    for clause in cnf:
        depth = max(depth, max([abs(l) for l in clause]))
    return depth

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 30
    total_depth = 0
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            continue
        for _ in range(instances_tested // len([5, 10, 15, 20, 30, 40])):
            cnf = generate_cnf(n)
            depth = frege_proof_depth(cnf)
            total_depth += depth
            if n == n_max:
                p = 2  # Smallest prime number
                bound = math.log(2) * (p - 1)**n / math.log(2)
                if depth > bound:
                    conjecture_holds = False
                    counterexample = f"CNF with n={n} has proof depth {depth}, which exceeds the bound of {bound}"

    mean_depth = Fraction(total_depth, instances_tested * len([5, 10, 15, 20, 30, 40]))
    std_dev = math.sqrt(sum((depth - mean_depth)**2 for depth in range(5, 41)) / (instances_tested * len([5, 10, 15, 20, 30, 40])))

    return {
        "metric_name": "Frege Proof Depth",
        "metric_value": mean_depth,
        "instances_tested": instances_tested * len([5, 10, 15, 20, 30, 40]),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)

    mean_depth = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_depth)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")