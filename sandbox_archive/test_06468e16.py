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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clauses = [c for c in clauses if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
        literals = [l for l in range(1, len(clauses)+1) if l not in assignment]
        literal = random.choice(literals)
        new_assignment[literal] = True
        if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
            return True
        new_assignment[literal] = False
        if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
            return True
        return False

    def hdeg(clauses):
        matroid_matrix = []
        for clause in clauses:
            row = [0] * (len(clause) + 1)
            for literal in clause:
                row[literal-1] = 1
            matroid_matrix.append(row)
        reduced_matrix = gaussian_elimination(matroid_matrix)
        rank = sum(1 for row in reduced_matrix if any(x != 0 for x in row))
        return len(clauses) - rank

    def dpll_diameter(clauses):
        assignment = {}
        stack = [(clauses, assignment)]
        max_depth = 0
        while stack:
            clauses, assignment = stack.pop()
            if not clauses:
                max_depth = max(max_depth, len(assignment))
                continue
            unit_clauses = [c for c in clauses if len(c) == 1]
            if unit_clauses:
                literal = unit_clauses[0][0]
                new_assignment = assignment.copy()
                new_assignment[literal] = True
                stack.append((clauses, new_assignment))
                new_assignment[literal] = False
                stack.append((clauses, new_assignment))
                continue
            literals = [l for l in range(1, len(clauses)+1) if l not in assignment]
            literal = random.choice(literals)
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            stack.append((clauses, new_assignment))
            new_assignment[literal] = False
            stack.append((clauses, new_assignment))
        return max_depth

    def generate_cnf(n):
        clauses = []
        for _ in range(2*n):
            clause = random.sample(range(1, n+1), 3)
            clauses.append(clause)
        return clauses

    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            cnf = generate_cnf(n)
            hdeg_value = hdeg(cnf)
            dpll_depth = dpll_diameter(cnf)
            results.append((hdeg_value, dpll_depth))

    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    hdeg_values = [r[0] for r in results]
    dpll_depths = [r[1] for r in results]

    n = len(results)
    mean_hdeg = sum(hdeg_values) / n
    mean_dpll = sum(dpll_depths) / n
    covariance = sum((hdeg_values[i] - mean_hdeg) * (dpll_depths[i] - mean_dpll) for i in range(n)) / n
    variance_hdeg = sum((hdeg_values[i] - mean_hdeg)**2 for i in range(n)) / n
    variance_dpll = sum((dpll_depths[i] - mean_dpll)**2 for i in range(n)) / n

    if variance_hdeg == 0 or variance_dpll == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": n,
            "n_max": max([r[1] for r in results]),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    pearson_corr = covariance / (variance_hdeg * variance_dpll)**0.5

    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": n,
        "n_max": max([r[1] for r in results]),
        "conjecture_holds": pearson_corr >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all(r["conjecture_holds"] for r in results):
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        if support_fraction >= 0.9:
            print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std={sum((r['metric_value'] - sum(r['metric_value'] for r in results) / len(results))**2 for r in results) / len(results)} support_fraction={support_fraction}")
        else:
            print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")