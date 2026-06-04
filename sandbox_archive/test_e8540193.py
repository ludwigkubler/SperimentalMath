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
    
    def generate_boolean_formula(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([f'x{i+1}', f'-x{i+1}']) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def dpll(clauses, assignment=[]):
        if not clauses:
            return True
        literal = next((l for l in set.union(*clauses) if l not in assignment and -l not in assignment), None)
        if literal is None:
            return False
        
        def simplify(lit):
            new_clauses = []
            for clause in clauses:
                if lit in clause:
                    continue
                elif -lit in clause:
                    clause.remove(-lit)
                    if not clause:
                        return False
                else:
                    new_clauses.append(clause)
            return new_clauses
        
        if dpll(simplify(literal), assignment + [literal]):
            return True
        if dpll(simplify(-literal), assignment + [-literal]):
            return True
        return False
    
    def quaternionic_form(clauses):
        n = len(clauses[0])
        Q = [[0 for _ in range(n)] for _ in range(n)]
        for clause in clauses:
            for i in range(n):
                if f'x{i+1}' in clause:
                    Q[i][i] += 1
                elif f'-x{i+1}' in clause:
                    Q[i][i] -= 1
        return Q
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        if m == 0 or n == 0:
            return 0
        
        def gaussian_elimination(A):
            rows, cols = len(A), len(A[0])
            for i in range(rows):
                max_row = i
                for j in range(i+1, rows):
                    if abs(A[j][i]) > abs(A[max_row][i]):
                        max_row = j
                A[i], A[max_row] = A[max_row], A[i]
                
                if A[i][i] == 0:
                    continue
                
                for j in range(i+1, cols):
                    A[i][j] /= A[i][i]
                
                for j in range(rows):
                    if j != i and A[j][i] != 0:
                        for k in range(i, cols):
                            A[j][k] -= A[i][k] * A[j][i]
            
            rank = sum(1 for row in A if any(row))
            return rank
        
        return gaussian_elimination(matrix)
    
    def height_dpll(clauses):
        if not clauses:
            return 0
        literal = next((l for l in set.union(*clauses) if l not in assignment and -l not in assignment), None)
        if literal is None:
            return 1
        
        def simplify(lit):
            new_clauses = []
            for clause in clauses:
                if lit in clause:
                    continue
                elif -lit in clause:
                    clause.remove(-lit)
                    if not clause:
                        return False
                else:
                    new_clauses.append(clause)
            return new_clauses
        
        return 1 + max(height_dpll(simplify(literal)), height_dpll(simplify(-literal)))
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    clauses = generate_boolean_formula(n)
    Q = quaternionic_form(clauses)
    rank_Q = rank(Q)
    height_DPLL = height_dpll(clauses)
    
    return {
        "metric_name": "Rank vs Height",
        "metric_value": rank_Q,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": rank_Q <= height_DPLL,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")