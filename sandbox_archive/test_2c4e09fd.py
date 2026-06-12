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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if i != j:
                    factor = Fraction(A[j][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def dpll_solver(clauses, assignment):
        if not clauses:
            return True
        if any(len(c) == 0 for c in clauses):
            return False
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if not dpll_solver([c - {literal} for c in clauses if literal in c], new_assignment):
                new_assignment[literal] = False
                return dpll_solver([c - {-literal} for c in clauses if -literal in c], new_assignment)
            return True
        pure_literal = next((l for l in range(1, max(clauses) + 1) if (l not in assignment and -l not in assignment)), None)
        if pure_literal:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            return dpll_solver([c - {pure_literal} for c in clauses if pure_literal in c], new_assignment)
        literal = random.choice(list(assignment.keys()))
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if not dpll_solver([c - {literal} for c in clauses if literal in c], new_assignment):
            new_assignment[literal] = False
            return dpll_solver([c - {-literal} for c in clauses if -literal in c], new_assignment)
        return True

    def quantum_invariant(clauses):
        n = max(abs(l) for l in set.union(*clauses))
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in clauses:
            for literal in clause:
                row, col = abs(literal), literal > 0
                A[row][col] += 1
        A = gaussian_elimination(A)
        min_order = sum(1 for row in A if any(x != 0 for x in row))
        return min_order

    def resolution_width(clauses):
        assignment = {}
        return dpll_solver(clauses, assignment)

    n_max = 40
    instances_tested = 0
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for n in range(5, 41, 5):
        for _ in range(6):  # Ensure at least 30 instances per seed
            clauses = []
            for _ in range(n * (n - 1) // 2):
                literals = random.sample(range(1, n + 1), 2)
                clause = {l if random.choice([True, False]) else -l for l in literals}
                clauses.append(clause)
            min_order = quantum_invariant(clauses)
            width = resolution_width(clauses)
            metric_values.append(min_order / width)
            instances_tested += 1
            n_max = max(n_max, n)

    if len(metric_values) < 30:
        return {
            "metric_name": "MinOrder/Width Ratio",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }

    correlation_coefficient = sum((x - mean) * (y - mean) for x, y in zip(metric_values, [sum(metric_values) / len(metric_values)] * len(metric_values))) / (len(metric_values) * math.sqrt(sum((x - mean) ** 2 for x in metric_values)) * math.sqrt(sum((y - mean) ** 2 for y in [sum(metric_values) / len(metric_values)] * len(metric_values))))
    if correlation_coefficient < 0.8:
        conjecture_holds = False
    if any(x / y < 0.5 for x, y in zip(metric_values, [sum(metric_values) / len(metric_values)] * len(metric_values))):
        counterexample = "min_order_too_small"

    return {
        "metric_name": "MinOrder/Width Ratio",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(r["counterexample"] != "" for r in results):
        first_failing_seed = next((r["seed"] for r in results if r["counterexample"] != ""), None)
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if r['counterexample'] != '')}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")