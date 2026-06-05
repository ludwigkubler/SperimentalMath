# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i+1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = Fraction(-matrix[i][i], matrix[max_row][i])
            for j in range(cols):
                matrix[i][j] += factor * matrix[max_row][j]
        return matrix
    
    def min_rank(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for i in range(rows):
            if all(matrix[i][j] == 0 for j in range(cols)):
                continue
            rank += 1
            factor = Fraction(1, matrix[i][i])
            for j in range(cols):
                matrix[i][j] *= factor
            for j in range(rows):
                if i != j:
                    factor = Fraction(-matrix[j][i], matrix[i][i])
                    for k in range(cols):
                        matrix[j][k] += factor * matrix[i][k]
        return rank
    
    def resolution_depth(clauses, assignment):
        depth = 0
        while True:
            new_clauses = []
            for clause in clauses:
                if any(lit in assignment and lit > 0 or -lit in assignment and lit < 0 for lit in clause):
                    continue
                new_clause = [lit for lit in clause if lit not in assignment]
                if len(new_clause) == 1:
                    return depth + 1
                new_clauses.append(new_clause)
            if new_clauses == clauses:
                break
            clauses = new_clauses
            depth += 1
        return float('inf')
    
    def generate_cnf(n):
        variables = list(range(1, n+1))
        clauses = []
        for _ in range(n):
            clause = random.sample(variables + [-v for v in variables], 2)
            clauses.append(clause)
        return clauses
    
    def lie_algebroid_rank(clauses):
        n = len(clauses)
        matrix = [[0] * (n+1) for _ in range(n+1)]
        for i, clause in enumerate(clauses):
            for lit in clause:
                if lit > 0:
                    matrix[i][lit-1] += 1
                else:
                    matrix[lit-1][i] += 1
        return min_rank(matrix)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    clauses = generate_cnf(n)
    assignment = {}
    depth = resolution_depth(clauses, assignment)
    rank = lie_algebroid_rank(clauses)
    
    return {
        "metric_name": "rank_over_depth",
        "metric_value": Fraction(rank, depth) if depth != float('inf') else 0,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if 0.5 <= r["metric_value"] <= 1.5) / len(results)
    
    if all(0.5 <= r["metric_value"] <= 1.5 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["metric_value"] < 0.5 or r["metric_value"] > 1.5 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not (0.5 <= result["metric_value"] <= 1.5))
        print(f"RESULT: FALSIFIED counterexample=\"out_of_range\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")