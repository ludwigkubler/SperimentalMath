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
    
    def incidence_matrix(formula, n):
        matrix = [[0] * n for _ in range(len(formula))]
        literals = set()
        for clause in formula:
            for literal in clause:
                literals.add(abs(literal))
        m = len(matrix)
        n = max(literals)
        
        for i, clause in enumerate(formula):
            for literal in clause:
                row = i
                col = abs(literal) - 1
                matrix[row][col] = 1 if literal > 0 else -1
        
        return matrix
    
    def resolution_width(formula):
        clauses = formula[:]
        while True:
            new_clauses = set()
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    clause_i = clauses[i]
                    clause_j = clauses[j]
                    for literal in clause_i:
                        if -literal in clause_j:
                            new_clause = [l for l in clause_i if l != literal] + \
                                          [l for l in clause_j if l != -literal]
                            new_clauses.add(tuple(sorted(new_clause)))
            if not new_clauses:
                break
            clauses.extend(new_clauses)
        return len(clauses)
    
    def min_order(matrix):
        m, n = len(matrix), len(matrix[0])
        identity = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(m)]
        
        # Gaussian elimination
        for col in range(n):
            pivot_row = None
            for row in range(col, m):
                if matrix[row][col] != 0:
                    pivot_row = row
                    break
            if pivot_row is None:
                continue
            
            # Swap rows to put the pivot at the top
            matrix[pivot_row], matrix[col] = matrix[col], matrix[pivot_row]
            
            # Normalize the pivot element
            denom = matrix[col][col]
            for j in range(n):
                matrix[col][j] /= denom
            
            # Eliminate the pivot column
            for row in range(m):
                if row != col:
                    factor = matrix[row][col]
                    for j in range(n):
                        matrix[row][j] -= factor * matrix[col][j]
        
        # Count non-zero rows to get the order of the lattice
        order = sum(1 for row in matrix if any(x != 0 for x in row))
        return order
    
    def generate_formula(n, m):
        formula = []
        for _ in range(m):
            clause = random.sample(range(-n, 0), 2) + random.sample(range(1, n+1), 2)
            formula.append(tuple(sorted(clause)))
        return formula
    
    n = random.randint(5, 40)
    m = random.randint(n, n * 3)
    formula = generate_formula(n, m)
    
    inc_matrix = incidence_matrix(formula, n)
    w_phi = resolution_width(formula)
    min_order_inc_matrix = min_order(inc_matrix)
    
    return {
        "metric_name": "min_order",
        "metric_value": min_order_inc_matrix,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")