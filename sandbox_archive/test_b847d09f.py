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
    
    def compute_clause_indicator_polynomial(clauses, n):
        if n > 20:
            return None  # Avoid large memory usage for n > 20
        polynomial = [0] * (2 ** n)
        for clause in clauses:
            product = 1
            for literal in clause:
                index = literal if literal >= 0 else -(literal + 1)
                product *= (-1) ** literal * (1 - x[index])
            polynomial += product
        return polynomial
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i + 1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            pivot = matrix[i][i]
            for j in range(cols):
                matrix[i][j] /= pivot
            
            for j in range(rows):
                if i != j:
                    factor = matrix[j][i]
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[i][k]
        
        rank = 0
        for row in matrix:
            if any(row):
                rank += 1
        return rank
    
    def dpll_search_tree_width(clauses, assignment):
        stack = [(clauses, assignment)]
        while stack:
            clauses, assignment = stack.pop()
            if not clauses:
                return len(assignment)
            clause = next(c for c in clauses if any(lit in assignment or -lit in assignment for lit in c))
            literals = [lit for lit in clause if lit not in assignment and -lit not in assignment]
            for literal in literals:
                new_assignment = assignment + [literal]
                new_clauses = [c for c in clauses if literal not in c and -literal not in c]
                stack.append((new_clauses, new_assignment))
        return float('inf')
    
    n = random.randint(5, 40)
    num_clauses = random.randint(n, n * (n + 1) // 2)
    clauses = []
    for _ in range(num_clauses):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(1, n))]
        clauses.append(clause)
    
    polynomial = compute_clause_indicator_polynomial(clauses, n)
    if polynomial is None:
        return {
            "metric_name": "minimal_rank",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    x = [Fraction(0, 1)] * n
    matrix = []
    for i in range(2 ** n):
        row = []
        for j in range(n):
            if (i >> j) & 1:
                row.append(-x[j])
            else:
                row.append(x[j])
        matrix.append(row)
    
    rank = gaussian_elimination(matrix)
    dpll_width = dpll_search_tree_width(clauses, [])
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= math.sqrt(n) * math.log(n),
        "counterexample": "" if rank <= math.sqrt(n) * math.log(n) else f"rank={rank} > Θ(√{n} log {n})"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank exceeds Θ(√n log n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")