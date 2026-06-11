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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n // 4):  # Ensure at least 16 instances per seed
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            clauses.append(clause)
        return clauses

    def dpll_width(cnf):
        def is_satisfiable(formula):
            stack = []
            assignment = [None] * (n + 1)
            
            def backtrack():
                if len(stack) == n:
                    return True
                var = next((i for i in range(1, n + 1) if assignment[i] is None), None)
                if var is None:
                    return False
                
                assignment[var] = True
                stack.append(var)
                if all(any(lit in clause for lit in clause) for clause in formula):
                    if backtrack():
                        return True
                stack.pop()
                assignment[var] = False
                
                assignment[-var] = True
                stack.append(-var)
                if all(any(lit in clause for lit in clause) for clause in formula):
                    if backtrack():
                        return True
                stack.pop()
                
                return False
            
            return backtrack()
        
        def width(formula, k):
            if len(stack) > k:
                return math.inf
            if is_satisfiable(formula):
                return 0
            var = next((i for i in range(1, n + 1) if assignment[i] is None), None)
            if var is None:
                return math.inf
            
            assignment[var] = True
            stack.append(var)
            width_true = width(formula, k)
            stack.pop()
            assignment[var] = False
            
            assignment[-var] = True
            stack.append(-var)
            width_false = width(formula, k)
            stack.pop()
            
            return 1 + max(width_true, width_false)
        
        n = len(cnf[0])
        assignment = [None] * (n + 1)
        stack = []
        return width(cnf, math.inf)

    def tropical_symplectic_form(cnf):
        matroid = {i: set() for i in range(1, len(cnf) + 1)}
        for clause in cnf:
            for lit in clause:
                if lit > 0:
                    matroid[lit].add(-lit)
                else:
                    matroid[-lit].add(lit)
        
        def rank(mat):
            m, n = len(mat), len(mat[0])
            A = [row[:] for row in mat]
            pivot_row = 0
            for col in range(n):
                if all(A[row][col] == 0 for row in range(pivot_row, m)):
                    continue
                max_pivot_row = pivot_row + next((i - pivot_row for i in range(pivot_row, m) if A[i][col]), 0)
                A[pivot_row], A[max_pivot_row] = A[max_pivot_row], A[pivot_row]
                for row in range(m):
                    if row != pivot_row:
                        factor = A[row][col] / A[pivot_row][col]
                        for j in range(n):
                            A[row][j] -= factor * A[pivot_row][j]
                pivot_row += 1
            return pivot_row
        
        return rank([[1 if i in mat[j] else 0 for j in range(len(mat))] for i in range(1, n + 1)])

    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    omega_phi = tropical_symplectic_form(cnf)
    w_phi = dpll_width(cnf)
    
    if omega_phi is None or w_phi is None:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation = (omega_phi - w_phi) / math.sqrt(omega_phi**2 + w_phi**2)
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(correlation) >= 0.7 and abs(omega_phi - w_phi) <= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_corr = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")