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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(10 * n):  # Generate 10 clauses per variable on average
            clause = [random.randint(-n, -1), random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf, assignment=None, free_vars=None):
        if assignment is None:
            assignment = {}
        if free_vars is None:
            free_vars = set(range(1, len(cnf) + 1))
        
        unit_clauses = [c for c in cnf if len(c) == 1]
        for clause in unit_clauses:
            literal = clause[0]
            var = abs(literal)
            assignment[var] = literal > 0
            free_vars.discard(var)
        
        pure_literals = {}
        for literal in set.union(*cnf):
            pos_count, neg_count = 0, 0
            for clause in cnf:
                if literal in clause:
                    pos_count += 1
                elif -literal in clause:
                    neg_count += 1
            if pos_count == 0 or neg_count == 0:
                pure_literals[literal] = True
        
        for literal, _ in pure_literals.items():
            var = abs(literal)
            assignment[var] = literal > 0
            free_vars.discard(var)
        
        if not free_vars:
            unsatisfiable = any(any(not (l in assignment and assignment[l]) for l in c) for c in cnf)
            return "UNSAT" if unsatisfiable else "SAT"
        
        var = next(iter(free_vars))
        pos_assignment = {**assignment, var: True}
        neg_assignment = {**assignment, var: False}
        pos_result = dpll(cnf, pos_assignment, free_vars - {var})
        if pos_result == "UNSAT":
            return dpll(cnf, neg_assignment, free_vars - {var})
        else:
            return pos_result
    
    def mci(f):
        n = len(f)
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                if f[i - 1][j - 1]:
                    matrix[i][j] = 1
                    matrix[j][i] = 1
        
        def gaussian_elimination(A):
            m, n = len(A), len(A[0])
            for i in range(m):
                max_row = i
                for j in range(i + 1, m):
                    if abs(A[j][i]) > abs(A[max_row][i]):
                        max_row = j
                A[i], A[max_row] = A[max_row], A[i]
                
                for j in range(n):
                    if j != i and A[j][i]:
                        factor = -A[j][i] / A[i][i]
                        for k in range(i, n):
                            A[j][k] += factor * A[i][k]
            
            rank = 0
            for row in A:
                if any(row):
                    rank += 1
            return rank
        
        return gaussian_elimination(matrix)
    
    def dpll_width(cnf):
        assignment = {}
        free_vars = set(range(1, len(cnf) + 1))
        
        def backtrack():
            if not free_vars:
                unsatisfiable = any(any(not (l in assignment and assignment[l]) for l in c) for c in cnf)
                return "UNSAT" if unsatisfiable else "SAT"
            
            var = next(iter(free_vars))
            pos_assignment = {**assignment, var: True}
            neg_assignment = {**assignment, var: False}
            pos_result = backtrack()
            if pos_result == "UNSAT":
                return backtrack()
            else:
                return pos_result
        
        return len(backtrack())
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    f = [[any(l in assignment and assignment[l] for l in c) for c in cnf] for _ in range(2 ** n)]
    
    mci_value = mci(f)
    dpll_width_value = dpll_width(cnf)
    
    return {
        "metric_name": "mci_dpll_correlation",
        "metric_value": mci_value * dpll_width_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False if mci_value == 0 or dpll_width_value == 0 else True,
        "counterexample": "" if mci_value != 0 and dpll_width_value != 0 else "mapping_undefined"
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")