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
    
    def generate_random_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf):
        if not cnf:
            return True
        literal = next((l for l in range(1, len(cnf) + 1) if l not in (set(x for x in clause if x > 0) | set(-x for x in clause if x < 0))), None)
        if literal is None:
            return False
        def propagate(lit):
            new_cnf = []
            for clause in cnf:
                if lit in clause:
                    continue
                if -lit in clause:
                    clause.remove(-lit)
                    if not clause:
                        return False
                else:
                    new_cnf.append(clause)
            return new_cnf
        if propagate(literal):
            if dpll(new_cnf):
                return True
        if propagate(-literal):
            if dpll(new_cnf):
                return True
        return False
    
    def frobenius_schur_indicator(matrix):
        n = len(matrix)
        trace = sum(matrix[i][i] for i in range(n))
        determinant = 1
        for row in matrix:
            determinant *= abs(row[0])
        return trace / determinant
    
    def resolution_width(cnf):
        clauses = cnf[:]
        width = 0
        while True:
            new_clause = None
            for clause1 in clauses:
                for literal1 in clause1:
                    if literal1 < 0:
                        continue
                    for clause2 in clauses:
                        if literal1 not in clause2:
                            continue
                        new_clause = [l for l in clause1 if l != literal1] + [l for l in clause2 if l != -literal1]
                        if len(new_clause) == 1:
                            return width
                        if len(new_clause) > width:
                            width = len(new_clause)
            if new_clause is None:
                break
            clauses.append(new_clause)
        return width
    
    def matrix_representation(cnf):
        n = len(cnf)
        matrix = [[0] * (2 * n) for _ in range(2 * n)]
        for i, clause in enumerate(cnf):
            for literal in clause:
                if literal > 0:
                    matrix[i][literal - 1] = 1
                else:
                    matrix[literal + n - 1][-literal - 1] = 1
        return matrix
    
    n = random.randint(5, 40)
    cnf = generate_random_cnf(n)
    
    matrix = matrix_representation(cnf)
    fsi = frobenius_schur_indicator(matrix)
    width = resolution_width(cnf)
    
    return {
        "metric_name": "Frobenius-Schur Indicator vs Resolution Width",
        "metric_value": abs(fsi - width),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False if abs(fsi - width) > 3 else True,
        "counterexample": "" if abs(fsi - width) <= 3 else f"FSI={fsi}, Width={width}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")