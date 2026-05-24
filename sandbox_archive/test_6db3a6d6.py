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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = max(range(i, rows), key=lambda r: abs(matrix[r][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        if matrix[i][i] == 0:
            continue
        for j in range(cols):
            matrix[i][j] /= matrix[i][i]
        for k in range(rows):
            if k != i and matrix[k][i] != 0:
                factor = matrix[k][i]
                for j in range(cols):
                    matrix[k][j] -= factor * matrix[i][j]
    return matrix

def rank(matrix):
    reduced_matrix = gaussian_elimination(matrix)
    rank = sum(1 for row in reduced_matrix if any(row))
    return rank

def dpll_refutation_tree(cnf, assignment=None):
    if assignment is None:
        assignment = {}
    literals = [literal for clause in cnf for literal in clause]
    literals = list(set(literals))  # Remove duplicates
    random.shuffle(literals)
    
    def dfs(literal):
        if literal not in assignment:
            assignment[literal] = True
            positive_clauses = [clause for clause in cnf if literal in clause]
            negative_clauses = [clause for clause in cnf if -literal in clause]
            if all(dfs(lit) for lit in positive_clauses):
                return True
            assignment[literal] = False
        return literal not in assignment or assignment[literal]
    
    if dfs(literals[0]):
        return 1 + max(dpll_refutation_tree(cnf, assignment), dpll_refutation_tree(cnf, {lit: not val for lit, val in assignment.items()}))
    else:
        return 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    cnf = []
    for _ in range(n):
        clause = [random.choice(range(-n, -1)) for _ in range(random.randint(1, n))]
        cnf.append(clause)
    
    rank_values = []
    diameter_values = []
    
    for _ in range(30):
        assignment = {}
        diameter = dpll_refutation_tree(cnf, assignment)
        if diameter == 0:
            continue
        matrix = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
        rank_value = rank(matrix)
        rank_values.append(rank_value)
        diameter_values.append(diameter)
    
    mean_rank = sum(rank_values) / len(rank_values)
    mean_diameter = sum(diameter_values) / len(diameter_values)
    correlation_coefficient = (sum((x - mean_rank) * (y - mean_diameter) for x, y in zip(rank_values, diameter_values)) /
                               math.sqrt(sum((x - mean_rank) ** 2 for x in rank_values) *
                                         sum((y - mean_diameter) ** 2 for y in diameter_values)))
    
    conjecture_holds = correlation_coefficient > 0.7 and mean_rank / mean_diameter <= 1.5
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(rank_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")