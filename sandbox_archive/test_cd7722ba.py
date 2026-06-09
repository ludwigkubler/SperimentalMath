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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, n):
            factor = -A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] += factor * A[i][k]
            b[j] += factor * b[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def solve_dpll(cnf):
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            var = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[var] = True
            if dpll([c for c in clauses if var not in c and -var not in c], new_assignment):
                return True
            new_assignment[var] = False
            if dpll([c for c in clauses if var not in c and -var not in c], new_assignment):
                return True
            return False
        pure_literal = next((v for v in range(1, max(cnf) + 1) if (v not in assignment and -v not in assignment)), None)
        if pure_literal:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            if dpll([c for c in clauses if pure_literal not in c and -pure_literal not in c], new_assignment):
                return True
            new_assignment[pure_literal] = False
            if dpll([c for c in clauses if pure_literal not in c and -pure_literal not in c], new_assignment):
                return True
            return False
        var = random.choice(list(assignment.keys()))
        new_assignment = assignment.copy()
        new_assignment[var] = True
        if dpll([c for c in clauses if var not in c and -var not in c], new_assignment):
            return True
        new_assignment[var] = False
        if dpll([c for c in clauses if var not in c and -var not in c], new_assignment):
            return True
        return False

    assignment = {}
    return dpll(cnf, assignment)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    total_morphisms = 0
    total_heights = 0

    for n in range(5, 41):
        for _ in range(7):  # Aim for at least 30 instances per seed
            m = random.randint(n // 2, n * (n - 1) // 2)
            cnf = []
            variables = set()
            for _ in range(m):
                clause = [random.choice([-i, i]) for i in range(1, n + 1)]
                cnf.append(clause)
                variables.update(abs(x) for x in clause)

            if not cnf:
                continue

            height = solve_dpll(cnf)
            morphisms = len(gaussian_elimination([[int(x > 0) - int(x < 0) for x in clause] for clause in cnf], [1] * m))
            
            total_morphisms += morphisms
            total_heights += height
            instances_tested += 1

    if instances_tested == 0:
        return {
            "metric_name": "Morphisms/Height Ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }

    ratio = Fraction(total_morphisms, total_heights)
    return {
        "metric_name": "Morphisms/Height Ratio",
        "metric_value": float(ratio),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": 0.5 <= ratio <= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std={0} support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(seeds) if not results[s]["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")