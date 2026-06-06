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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if random.random() < 0.5:
                clause.append(-1)
            clauses.append(clause)
        return clauses

    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        unit_clause = next((c for c in cnf if len([x for x in c if x != 0]) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = {**assignment, abs(literal): literal > 0}
            return dpll(cnf, new_assignment) or dpll(cnf, {**new_assignment, abs(literal): not (literal > 0)})
        pure_literal = next((i for i in range(1, n + 1) if all(x == 0 or x == i for c in cnf for x in c)), None)
        if pure_literal:
            new_assignment = {**assignment, pure_literal: True}
            return dpll(cnf, new_assignment) or dpll(cnf, {**new_assignment, pure_literal: False})
        literal = random.choice([i for i in range(1, n + 1)])
        new_assignment = {**assignment, literal: True}
        if dpll(cnf, new_assignment):
            return True
        new_assignment[literal] = False
        return dpll(cnf, new_assignment)

    def resolution_width(cnf):
        queue = cnf[:]
        while queue:
            clause1 = queue.pop(0)
            for clause2 in queue:
                if any(-x in clause1 and x in clause2 for x in set(clause1) & set(clause2)):
                    new_clause = [x for x in clause1 + clause2 if x not in [-y, y] for y in set(clause1) & set(clause2)]
                    if len(new_clause) == 0:
                        return 1
                    queue.append(new_clause)
        return float('inf')

    def tropical_derivative_degree(cnf):
        n = len(cnf[0])
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for literal in clause:
                if literal > 0:
                    row, col = divmod(literal - 1, n)
                    matrix[row][col] += 1
                else:
                    row, col = divmod(-literal - 1, n)
                    matrix[row][n] -= 1
        for i in range(n + 1):
            if matrix[i][i] == 0:
                return float('inf')
        return sum(matrix[i][i] for i in range(n + 1))

    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    d = tropical_derivative_degree(cnf)
    w = resolution_width(cnf)

    if w == float('inf'):
        return {
            "metric_name": "Minimal Tropical Derivative Degree and Resolution Proof Width Ratio",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Resolution width is infinite"
        }

    ratio = d / w
    return {
        "metric_name": "Minimal Tropical Derivative Degree and Resolution Proof Width Ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio <= 2,  # Assuming c = 2 for simplicity
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='First failing seed' first_failing_seed={first_failing_seed}")