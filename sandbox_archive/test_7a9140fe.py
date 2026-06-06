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
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def dpll(clauses, assignment=None):
    if not clauses:
        return assignment
    variables = set()
    for clause in clauses:
        variables.update(abs(l) for l in clause)
    unit_clause = next((c for c in clauses if len(c) == 1), None)
    if unit_clause:
        literal = unit_clause[0]
        new_assignment = assignment.copy() if assignment else {}
        new_assignment[literal] = literal > 0
        return dpll(clauses, new_assignment)
    pure_literal = next((l for l in variables if all(l in c or f'-{l}' in c for c in clauses)), None)
    if pure_literal:
        new_assignment = assignment.copy() if assignment else {}
        new_assignment[pure_literal] = True
        return dpll(clauses, new_assignment)
    literal = next(iter(variables))
    new_clauses_true = [c for c in clauses if literal not in c and f'-{literal}' not in c]
    result_true = dpll(new_clauses_true, assignment)
    if result_true:
        return result_true
    new_clauses_false = [c for c in clauses if f'-{literal}' not in c]
    result_false = dpll(new_clauses_false, {**assignment, literal: False})
    return result_false

def tseytin_transform(n):
    variables = list(range(1, 2*n + 1))
    clauses = []
    for i in range(1, n + 1):
        clauses.append([i, -i + n])
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            clauses.append([-i, -j, i + j - 1])
    return variables, clauses

def dpll_path_length(clauses):
    assignment = {}
    stack = []
    def backtrack():
        if not clauses:
            return len(stack)
        literal = next((l for l in range(1, 2*n + 1) if all(l in c or f'-{l}' in c for c in clauses)), None)
        if literal is None:
            return float('inf')
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        stack.append((literal, True))
        result = backtrack()
        if result < float('inf'):
            return result
        del new_assignment[literal]
        stack.pop()
        new_assignment[literal] = False
        stack.append((literal, False))
        result = backtrack()
        if result < float('inf'):
            return result
        del new_assignment[literal]
        stack.pop()
        return float('inf')
    n = len(clauses)
    return backtrack()

def run_trial(seed: int) -> dict:
    random.seed(seed)
    variables, clauses = tseytin_transform(10)
    mgm = 0.0
    l = dpll_path_length(clauses)
    if l == float('inf'):
        return {
            "metric_name": "DPLL Proof Path Length",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": 10,
            "conjecture_holds": False,
            "counterexample": "Unsolvable instance"
        }
    return {
        "metric_name": "DPLL Proof Path Length",
        "metric_value": l,
        "instances_tested": 1,
        "n_max": 10,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result_type = "SUPPORTED"
    else:
        mean_value = None
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        result_type = "FALSIFIED"

    print(f"RESULT: {result_type} mean={mean_value} std=None support_fraction={support_fraction}")