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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i+1}' for i in range(n)]
        clauses = []
        for var in variables:
            clauses.append([var, f'~{var}'])
        for i in range(1, n):
            clauses.append([f'~{variables[i-1]}', variables[i]])
        return variables, clauses
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for col in range(cols):
            pivot_row = None
            for row in range(col, rows):
                if matrix[row][col] != 0:
                    pivot_row = row
                    break
            if pivot_row is None:
                continue
            matrix[pivot_row], matrix[col] = matrix[col], matrix[pivot_row]
            for row in range(rows):
                if row == col:
                    continue
                factor = -matrix[row][col] / matrix[col][col]
                for j in range(cols):
                    matrix[row][j] += factor * matrix[col][j]
        rank = sum(1 for row in matrix if any(row[j] != 0 for j in range(cols)))
        return rank
    
    def resolution_length(clauses):
        stack = clauses[:]
        while True:
            new_clause = None
            for i in range(len(stack)):
                for j in range(i + 1, len(stack)):
                    clause1 = set(stack[i])
                    clause2 = set(stack[j])
                    if any(-x in clause2 for x in clause1):
                        new_clause = [x for x in clause1 ^ clause2 if x > 0]
                        break
                if new_clause is not None:
                    break
            if new_clause is None:
                return len(clauses)
            stack.append(new_clause)
    
    n = random.randint(5, 40)
    variables, clauses = generate_tseitin_formula(n)
    incidence_matrix = [[1 if var in clause else 0 for var in variables] for clause in clauses]
    rank = gaussian_elimination(incidence_matrix)
    resolution_len = resolution_length(clauses)
    
    return {
        "metric_name": "Minimal Rank vs Resolution Proof Length",
        "metric_value": rank * resolution_len,
        "instances_tested": 1,
        "conjecture_holds": rank <= n**(2/3) * math.log(n)**2 and resolution_len >= rank,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")