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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i
        for k in range(i + 1, rows):
            if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                max_row = k
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        factor = Fraction(-matrix[i][i], matrix[max_row][i])
        for j in range(cols):
            matrix[max_row][j] *= factor
        for k in range(rows):
            if k != max_row:
                factor = Fraction(matrix[k][i], matrix[max_row][i])
                for j in range(cols):
                    matrix[k][j] += factor * matrix[max_row][j]
    rank = 0
    for row in matrix:
        if any(row[i] != 0 for i in range(cols)):
            rank += 1
    return rank

def dpll(cnf, assignment={}):
    if not cnf:
        return True
    unit_clause = next((c for c in cnf if len(c) == 1), None)
    if unit_clause:
        literal = unit_clause[0]
        new_assignment = {**assignment, abs(literal): literal > 0}
        if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
            return True
        else:
            del new_assignment[abs(literal)]
    literals = [l for clause in cnf for l in clause]
    literal = random.choice(list(set(literals)))
    new_assignment = {**assignment, abs(literal): literal > 0}
    if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
        return True
    else:
        del new_assignment[abs(literal)]
    return False

def resolution(cnf):
    clauses = set(tuple(sorted(clause)) for clause in cnf)
    while True:
        new_clauses = set()
        for a, b in itertools.combinations(clauses, 2):
            if len(set(a) & set(b)) == 1:
                literal = (set(a) - set(b)).pop()
                new_clause = tuple(sorted(c for c in a + b if c != literal and -c not in a + b))
                if not new_clause:
                    return True
                new_clauses.add(new_clause)
        if new_clauses.issubset(clauses):
            break
        clauses.update(new_clauses)
    return False

def rank(cnf):
    n = len(cnf[0])
    matrix = [[0] * (n + 1) for _ in range(n)]
    for i, clause in enumerate(cnf):
        for literal in clause:
            if literal > 0:
                matrix[literal - 1][i] = 1
            else:
                matrix[-literal - 1][i] = -1
    return gaussian_elimination(matrix)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n * (n - 1), n * n)
    cnf = []
    for _ in range(m):
        clause = [random.choice([-i, i]) for i in range(1, n + 1)]
        if random.random() < 0.5:
            clause.append(random.choice([-i, i]))
        cnf.append(clause)
    
    rank_value = rank(cnf)
    resolution_width = resolution(cnf)
    
    return {
        "metric_name": "Correlation",
        "metric_value": rank_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": rank_value == resolution_width,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")