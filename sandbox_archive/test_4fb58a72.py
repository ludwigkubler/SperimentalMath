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
        literals = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for literal in literals:
            clauses.append([literal])
        for i in range(n):
            for j in range(i+1, n):
                clauses.append([f'~{literals[i]}', f'~{literals[j]}', f'x{i+j+1}'])
                clauses.append([f'{literals[i]}', f'{literals[j]}', f'~x{i+j+1}'])
        return literals, clauses
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i+1, rows):
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
        return matrix
    
    def min_rank(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for i in range(min(rows, cols)):
            if all(abs(matrix[j][i]) < 1e-9 for j in range(rank)):
                continue
            rank += 1
            for j in range(i+1, rows):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(cols):
                    matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    def resolution_refutation_size(clauses):
        clauses_set = set(tuple(sorted(c)) for c in clauses)
        refutation = []
        while True:
            new_clause = None
            for c1, c2 in itertools.combinations(clauses_set, 2):
                if any(lit in c1 and '~' + lit in c2 for lit in literals):
                    new_clause = [lit for lit in c1 if lit not in c2] + [lit[1:] for lit in c2 if '~' + lit in c1]
                    break
            if new_clause is None:
                break
            clauses_set.add(tuple(sorted(new_clause)))
            refutation.append(new_clause)
        return len(refutation)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    literals, clauses = generate_tseitin_formula(n)
    matrix = [[int(lit in clause) for lit in literals] for clause in clauses]
    k_theory_rank = min_rank(matrix)
    refutation_size = resolution_refutation_size(clauses)
    
    return {
        "metric_name": "Resolution Refutation Size",
        "metric_value": refutation_size,
        "instances_tested": 1,
        "conjecture_holds": k_theory_rank >= 2**(1/4) * n,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 17 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results]
    conjecture_holds = all(r["conjecture_holds"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if conjecture_holds and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values)} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values))} support_fraction={support_fraction}")
    elif not conjecture_holds and any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"K-theory rank too low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")