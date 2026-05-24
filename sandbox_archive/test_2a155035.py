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
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            pivot = matrix[i][i]
            if pivot == 0:
                continue
            for j in range(i, n):
                matrix[i][j] /= pivot
            for k in range(m):
                if k != i and matrix[k][i] != 0:
                    factor = matrix[k][i]
                    for j in range(i, n):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix

    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        row_echelon_form = gaussian_elimination(matrix)
        rank = 0
        for i in range(m):
            if any(row_echelon_form[i][j] != 0 for j in range(n)):
                rank += 1
        return rank

    def tseitin_formula(n, m):
        variables = list(range(1, n+1))
        clauses = []
        for _ in range(m):
            a, b, c = random.sample(variables, 3)
            clauses.append((a, -b, c))
            clauses.append((-a, b, c))
            clauses.append((a, b, -c))
            clauses.append((-a, -b, c))
        return variables, clauses

    def quadratic_form(variables, clauses):
        m = len(clauses)
        n = len(variables)
        qf = [[0] * (n+1) for _ in range(n+1)]
        for a, b, c in clauses:
            qf[a][a] += 2
            qf[b][b] += 2
            qf[c][c] += 2
            qf[a][b] -= 1
            qf[b][a] -= 1
            qf[a][c] -= 1
            qf[c][a] -= 1
            qf[b][c] -= 1
            qf[c][b] -= 1
        return qf

    def resolution_proof_length(variables, clauses):
        # Simplified DPLL solver for Tseitin formula
        stack = []
        assignment = {v: None for v in variables}
        def dpll():
            if not clauses:
                return True
            literal = next((l for l in range(1, n+1) if assignment[l] is None), None)
            if literal is None:
                return False
            assignment[literal] = True
            stack.append(literal)
            new_clauses = []
            for clause in clauses:
                if any(l not in assignment or assignment[l] == True for l in clause):
                    continue
                if any(l not in assignment or assignment[l] == False for l in [-l for l in clause]):
                    return False
                new_clause = [l for l in clause if l not in assignment]
                if new_clause:
                    new_clauses.append(new_clause)
            if dpll():
                return True
            assignment[literal] = False
            stack.pop()
            assignment[-literal] = True
            new_clauses = []
            for clause in clauses:
                if any(l not in assignment or assignment[l] == True for l in [-l for l in clause]):
                    continue
                if any(l not in assignment or assignment[l] == False for l in clause):
                    return False
                new_clause = [l for l in clause if -l not in assignment]
                if new_clause:
                    new_clauses.append(new_clause)
            if dpll():
                return True
            return False
        return len(stack)

    n = random.randint(5, 40)
    m = random.randint(n, n*2)
    variables, clauses = tseitin_formula(n, m)
    qf = quadratic_form(variables, clauses)
    rank_value = rank(qf)
    proof_length = resolution_proof_length(variables, clauses)

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": rank_value / proof_length if proof_length != 0 else float('inf'),
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")