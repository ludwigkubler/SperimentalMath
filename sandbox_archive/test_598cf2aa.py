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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for var in variables:
            clauses.append([var])
        for i in range(2, n+1):
            clauses.append([f'x{i}', f'~x{i-1}'])
        return variables, clauses
    
    def incidence_matrix(variables, clauses):
        m = len(clauses)
        n = len(variables)
        matrix = [[0] * (n + 1) for _ in range(m)]
        for i, clause in enumerate(clauses):
            for var in clause:
                if var.startswith('~'):
                    j = int(var[2:]) - 1
                    matrix[i][j+1] = -1
                else:
                    j = int(var[1:]) - 1
                    matrix[i][j+1] = 1
        return matrix
    
    def min_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(n):
            if all(matrix[j][i] == 0 for j in range(m)):
                continue
            rank += 1
            for j in range(m):
                if matrix[j][i] != 0:
                    pivot_row = j
                    break
            for k in range(n):
                matrix[pivot_row][k], matrix[i][k] = matrix[i][k], matrix[pivot_row][k]
            for j in range(m):
                if j == i:
                    continue
                factor = -matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] += factor * matrix[i][k]
        return rank
    
    def dpll_width(clauses, assignment):
        stack = []
        while True:
            if all(c in assignment for c in clauses):
                return len(assignment)
            unit_clause = next((c for c in clauses if len([x for x in c if x not in assignment and '~' + x not in assignment]) == 1), None)
            if unit_clause is None:
                return float('inf')
            var = [v for v in unit_clause if v not in assignment and '~' + v not in assignment][0]
            assignment[var] = True
            stack.append((var, False))
            while stack:
                var, negated = stack.pop()
                if negated:
                    del assignment[var]
                else:
                    assignment['~' + var] = True
                    for c in clauses:
                        if all(x not in assignment and '~' + x not in assignment for x in c):
                            continue
                        if any(x in assignment and assignment[x] == (not negated) for x in c):
                            stack.append((var, True))
                            break
                    else:
                        stack.append((var, False))
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    variables, clauses = generate_tseitin_formula(n)
    matrix = incidence_matrix(variables, clauses)
    R_F = min_rank(matrix)
    
    assignment = {}
    w_F = dpll_width(clauses, assignment)
    
    if w_F == float('inf'):
        return {
            "metric_name": "R(F) / w*(F)",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "DPLL proof width is infinite"
        }
    
    ratio = R_F / w_F
    return {
        "metric_name": "R(F) / w*(F)",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        if result["metric_value"] is not None:
            results.append(result["metric_value"])
    
    mean_ratio = sum(results) / len(results)
    std_ratio = math.sqrt(sum((x - mean_ratio)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r <= 1.2) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(r > 1.2 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result > 1.2)
        print(f"RESULT: FALSIFIED counterexample='R(F) / w*(F) > 1.2' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support for conjecture")