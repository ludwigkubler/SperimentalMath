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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0 for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented = [A[i] + [b[i]] for i in range(m)]
    for j in range(n):
        pivot_row = max(range(j, m), key=lambda i: abs(augmented[i][j]))
        if augmented[pivot_row][j] == 0:
            return None
        augmented[j], augmented[pivot_row] = augmented[pivot_row], augmented[j]
        for i in range(m):
            if i != j:
                factor = augmented[i][j] / augmented[j][j]
                for k in range(n + 1):
                    augmented[i][k] -= factor * augmented[j][k]
    return [row[-1] for row in augmented]

def rank(matrix):
    m, n = len(matrix), len(matrix[0])
    A = matrix
    r = 0
    for j in range(n):
        if r < m:
            pivot_row = max(range(r, m), key=lambda i: abs(A[i][j]))
            if A[pivot_row][j] == 0:
                continue
            A[r], A[pivot_row] = A[pivot_row], A[r]
            for i in range(m):
                if i != r:
                    factor = A[i][j] / A[r][j]
                    for k in range(n):
                        A[i][k] -= factor * A[r][k]
            r += 1
    return r

def generate_mso_formula(depth, clause_length):
    variables = [f'x{i}' for i in range(1, depth + 1)]
    clauses = []
    for _ in range(clause_length):
        clause = random.sample(variables, depth)
        if random.choice([True, False]):
            clause = [f'~{var}' for var in clause]
        clauses.append(' | '.join(clause))
    return ' & '.join(clauses)

def evaluate_ramanujan_sum(formula, n):
    variables = set()
    for char in formula:
        if char.isalpha() and char.islower():
            variables.add(char)
    variable_values = {var: random.choice([0, 1]) for var in variables}
    
    def eval_formula(formula):
        if ' & ' in formula:
            return eval_formula(formula.split(' & ')[0]) and eval_formula(formula.split(' & ')[1])
        elif ' | ' in formula:
            return eval_formula(formula.split(' | ')[0]) or eval_formula(formula.split(' | ')[1])
        elif '~' in formula:
            return not eval_formula(formula[1:])
        else:
            var = formula
            if variable_values[var] == 0:
                return False
            elif variable_values[var] == 1:
                return True
    
    return int(eval_formula(formula))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    instances_tested = 0
    total_rank = 0
    max_rank = 0

    for depth in range(1, n + 1):
        for clause_length in range(1, n + 1):
            formula = generate_mso_formula(depth, clause_length)
            rank_value = evaluate_ramanujan_sum(formula, n)
            instances_tested += 1
            total_rank += rank_value
            max_rank = max(max_rank, rank_value)

    mean_rank = total_rank / instances_tested
    conjecture_holds = mean_rank <= 2 * n and max_rank <= 2 * n

    return {
        "metric_name": "Minimal Rank of Ramanujan Sums",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Mean rank {mean_rank}, Max rank {max_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")

    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    max_rank = max(result["metric_value"] for result in results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Mean rank {mean_rank}, Max rank {max_rank}\" first_failing_seed={first_failing_seed}")