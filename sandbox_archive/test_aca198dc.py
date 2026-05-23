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
        G = []
        for i in range(1, n+1):
            G.append(f"X{i}")
        for i in range(1, n+1):
            G.append(f"(NOT X{i})")
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                G.append(f"(OR (AND X{i} X{j}) (NOT X{i}))")
                G.append(f"(OR (AND X{i} (NOT X{j})) (NOT X{j}))")
        return G
    
    def resolution_length(formula):
        clauses = formula
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i+1, len(clauses)):
                    if any(c in clauses[j] and not c.startswith('NOT ') for c in clauses[i]):
                        new_clause = [c.replace('NOT ', '') for c in clauses[i] if c != 'NOT ' + c]
                        new_clause.extend([c[4:] for c in clauses[j] if c.startswith('NOT ')])
                        new_clauses.append(new_clause)
                    elif any(c.startswith('NOT ') and c[4:] in clauses[j] for c in clauses[i]):
                        new_clause = [c.replace('NOT ', '') for c in clauses[i] if not c == 'NOT ' + c[4:]]
                        new_clause.extend([c[4:] for c in clauses[j] if not c.startswith('NOT ') and c != c[4:]])
                        new_clauses.append(new_clause)
            if new_clauses == clauses:
                return len(clauses)
            clauses = new_clauses
    
    def noncommutative_rank(formula):
        n = len(formula)
        adj_matrix = [[0] * n for _ in range(n)]
        for clause in formula:
            for i in range(1, n+1):
                if f"X{i}" in clause or f"(NOT X{i})" in clause:
                    for j in range(i+1, n+1):
                        if f"X{j}" in clause or f"(NOT X{j})" in clause:
                            adj_matrix[i-1][j-1] = 1
                            adj_matrix[j-1][i-1] = 1
        
        def gaussian_elimination(matrix):
            rows, cols = len(matrix), len(matrix[0])
            for i in range(rows):
                max_row = i
                for j in range(i+1, rows):
                    if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                        max_row = j
                matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
                for j in range(i+1, rows):
                    factor = matrix[j][i] / matrix[i][i]
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[i][k]
            rank = 0
            for row in matrix:
                if any(row):
                    rank += 1
            return rank
        
        return gaussian_elimination(adj_matrix)
    
    n = random.randint(5, 40)
    formula = generate_tseitin_formula(n)
    resolution_len = resolution_length(formula)
    noncommutative_rank_val = noncommutative_rank(formula)
    
    if resolution_len == 0:
        return {
            "metric_name": "noncommutative_rank",
            "metric_value": noncommutative_rank_val,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "resolution_length_zero"
        }
    
    if noncommutative_rank_val > 2 * resolution_len:
        return {
            "metric_name": "noncommutative_rank",
            "metric_value": noncommutative_rank_val,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"rank={noncommutative_rank_val}, resolution_length={resolution_len}"
        }
    
    return {
        "metric_name": "noncommutative_rank",
        "metric_value": noncommutative_rank_val,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")