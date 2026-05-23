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
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def dpll_width(clauses, assignment):
        stack = []
        while True:
            unit_clause = None
            for clause in clauses:
                unsatisfied = [var for var in clause if var not in assignment and -var not in assignment]
                if len(unsatisfied) == 1:
                    unit_clause = unsatisfied[0]
                    break
            if unit_clause is None:
                if all(var in assignment or -var in assignment for clause in clauses):
                    return len(stack)
                else:
                    return math.inf
            stack.append(unit_clause)
            assignment[unit_clause] = True
            new_clauses = []
            for clause in clauses:
                if not any(var in assignment and assignment[var] == True for var in clause):
                    new_clauses.append([var for var in clause if var != unit_clause])
            clauses = new_clauses
    
    def min_reflections(clause):
        return len(set(abs(var) for var in clause))
    
    n = random.randint(5, 40)
    variables = list(range(-n, 0)) + list(range(1, n+1))
    clauses = []
    for _ in range(n * (n - 1)):
        clause = [random.choice(variables) for _ in range(random.randint(2, n))]
        if random.choice([True, False]):
            clause.append(-random.choice(variables))
        clauses.append(clause)
    
    A = [[0] * (2*n) for _ in range(n)]
    for i in range(n):
        for var in variables:
            if var == i + 1 or -var == i + 1:
                A[i][i + n] = 1
            else:
                A[i][i + n] = 0
    
    width_sum = 0
    reflections_sum = 0
    instances_tested = 0
    
    for _ in range(30):
        assignment = {}
        width = dpll_width(clauses, assignment)
        if width < math.inf:
            reflections = min_reflections(random.choice(clauses))
            width_sum += width
            reflections_sum += reflections
            instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "width",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }
    
    width_avg = width_sum / instances_tested
    reflections_avg = reflections_sum / instances_tested
    
    return {
        "metric_name": "width",
        "metric_value": width_avg,
        "instances_tested": instances_tested,
        "conjecture_holds": abs(width_avg - reflections_avg) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std = math.sqrt(sum((r["metric_value"] - mean)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any("conjecture_holds" in r and not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "conjecture_holds" in result and not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_valid_instances")