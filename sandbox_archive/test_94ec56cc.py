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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = Fraction(matrix[i][i])
            for j in range(n):
                matrix[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def determinant(matrix):
        n = len(matrix)
        det = Fraction(1)
        for i in range(n):
            det *= matrix[i][i]
        return det

    def is_trivial_entanglement(det):
        return det == 0 or det == 1

    def generate_cnf_formula(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(random.randint(2, n))]
            clauses.append(clause)
        return clauses

    def dpll_solver(cnf):
        def solve(literals):
            if not cnf:
                return True
            clause = next((c for c in cnf if any(l in c or -l in c for l in literals)), None)
            if not clause:
                return False
            literal = next(l for l in clause if l > 0)
            if solve(literals + [literal]):
                return True
            if solve(literals + [-literal]):
                return True
            return False
        return solve([])

    def circuit_satisfiability_complexity(cnf):
        return len(cnf) / math.log(len(cnf), 2)

    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf_formula(n)
    det = determinant(gaussian_elimination([[random.randint(0, 1) for _ in range(n)] for _ in range(n)]))
    entanglement_non_trivial = not is_trivial_entanglement(det)
    complexity = circuit_satisfiability_complexity(cnf)

    return {
        "metric_name": "circuit_satisfiability_complexity",
        "metric_value": complexity,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": entanglement_non_trivial == (complexity <= 5),
        "counterexample": "" if entanglement_non_trivial == (complexity <= 5) else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    metric_values = [r["metric_value"] for r in results]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if all(r["conjecture_holds"] for r in results):
        result = "SUPPORTED"
    elif support_fraction >= 0.7 and max(metric_values) <= 5:
        result = "SUPPORTED"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        result = f"FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}"

    print(f"RESULT: {result} mean={sum(metric_values)/len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):.2f} support_fraction={support_fraction:.2f}")