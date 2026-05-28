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
    
    def generate_tseitin_formula(n, m):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(m):
            clause = random.sample(variables + ['~' + v for v in variables], 2)
            if random.choice([True, False]):
                clause.append('~' + random.choice(clause))
            clauses.append(' | '.join(clause))
        return ' & '.join(clauses)

    def parse_formula(formula):
        literals = set()
        for clause in formula.split(' & '):
            for literal in clause.split(' | '):
                if literal.startswith('~'):
                    literals.add(literal[1:])
                else:
                    literals.add(literal)
        return literals

    def gaussian_elimination(matrix, b):
        n = len(matrix)
        augmented_matrix = [row + [b[i]] for i, row in enumerate(matrix)]
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                    max_row = j
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            pivot = augmented_matrix[i][i]
            for j in range(i, n+1):
                augmented_matrix[i][j] /= pivot
            for j in range(n):
                if j != i:
                    factor = augmented_matrix[j][i]
                    for k in range(i, n+1):
                        augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
        return [row[-1] for row in augmented_matrix]

    def rank(matrix):
        n = len(matrix)
        m = len(matrix[0])
        rref = []
        pivot_columns = set()
        for i in range(n):
            if i not in pivot_columns:
                max_row = i
                for j in range(i+1, n):
                    if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                        max_row = j
                matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
                pivot_columns.add(i)
                rref.append([matrix[i][j]/matrix[i][i] for j in range(m)])
            else:
                rref.append([0]*m)
        return len(pivot_columns)

    def resolution_length(formula):
        literals = parse_formula(formula)
        clauses = formula.split(' & ')
        resolution_steps = 0
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i+1, len(clauses)):
                    clause_i = set(clause.split(' | ') for clause in clauses[i].split(' & '))
                    clause_j = set(clause.split(' | ') for clause in clauses[j].split(' & '))
                    new_clause = []
                    for literal in literals:
                        if literal not in clause_i and '~' + literal not in clause_j:
                            new_clause.append(literal)
                        elif literal not in clause_j and '~' + literal not in clause_i:
                            new_clause.append('~' + literal)
                    if len(new_clause) > 0:
                        new_clauses.append(' | '.join(new_clause))
            if len(new_clauses) == 0:
                break
            clauses += new_clauses
            resolution_steps += 1
        return resolution_steps

    n = random.randint(5, 40)
    m = random.randint(n**2, n**3)
    formula = generate_tseitin_formula(n, m)
    
    matrix = []
    for clause in formula.split(' & '):
        row = [0] * (n + 1)
        for literal in clause.split(' | '):
            if literal.startswith('~'):
                var_index = int(literal[1:]) - 1
                row[var_index] = -1
            else:
                var_index = int(literal) - 1
                row[var_index] = 1
        matrix.append(row)
    
    b = [1] * (n + 1)
    solution = gaussian_elimination(matrix, b)
    
    R_G = rank(matrix)
    resolution_steps = resolution_length(formula)
    
    metric_value = 2 ** (R_G / n**2)
    conjecture_holds = resolution_steps >= metric_value
    counterexample = "" if conjecture_holds else f"Formula: {formula}, Resolution Steps: {resolution_steps}, Metric Value: {metric_value}"
    
    return {
        "metric_name": "Resolution Proof Length",
        "metric_value": resolution_steps,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 89))  # First 30 primes
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")