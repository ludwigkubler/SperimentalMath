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

def generate_tseitin_formula(n: int, m: int):
    literals = [f'x{i}' for i in range(1, n + 1)]
    variables = literals[:]
    clauses = []

    # Generate OR clauses
    for _ in range(m // 2):
        clause = random.sample(literals, 2)
        clauses.append(clause)

    # Generate AND clauses
    for _ in range((m - m // 2) // 3):
        clause = random.sample(literals, 3)
        clauses.append(clause)

    return variables, clauses

def incidence_matrix(variables, clauses):
    n = len(variables)
    m = len(clauses)
    matrix = [[0] * (n + m) for _ in range(n + m)]

    for i, clause in enumerate(clauses):
        for literal in clause:
            if literal.startswith('x'):
                j = variables.index(literal)
                matrix[j][i + n] = 1
            else:
                j = variables.index(literal[1:])
                matrix[j][i + n] = -1

    return matrix

def min_rank(matrix):
    n, m = len(matrix), len(matrix[0])
    rank = 0
    for i in range(n):
        if any(matrix[i]):
            pivot_col = next(j for j in range(m) if matrix[i][j] != 0)
            rank += 1
            for k in range(n):
                if k != i and matrix[k][pivot_col] != 0:
                    factor = Fraction(matrix[k][pivot_col], matrix[i][pivot_col])
                    for j in range(m):
                        matrix[k][j] -= factor * matrix[i][j]
    return rank

def dpll_proof_width(clauses, variables):
    n = len(variables)
    m = len(clauses)
    stack = []
    assignment = [None] * (n + m)

    def backtrack(level):
        if level == n:
            for clause in clauses:
                if not any(assignment[i] is None or (assignment[i] and literal.startswith('x')) or (not assignment[i] and literal[1:] in variables) for literal in clause):
                    return False
            return True

        var = variables[level]
        assignment[level] = True
        stack.append((level, True))
        if backtrack(level + 1):
            return True
        stack.pop()

        assignment[level] = False
        stack.append((level, False))
        if backtrack(level + 1):
            return True
        stack.pop()

        return False

    return len(stack)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = 2 * n
        variables, clauses = generate_tseitin_formula(n, m)
        matrix = incidence_matrix(variables, clauses)
        R_F = min_rank(matrix)
        w_star_F = dpll_proof_width(clauses, variables)
        
        if w_star_F == 0:
            continue
        
        ratio = Fraction(R_F, w_star_F)
        results.append(ratio)
    
    mean_ratio = sum(results) / len(results)
    std_ratio = (sum((x - mean_ratio) ** 2 for x in results) / len(results)) ** 0.5
    
    conjecture_holds = mean_ratio <= Fraction(12, 10) and std_ratio <= Fraction(1, 10)
    counterexample = "" if conjecture_holds else f"mean_ratio={mean_ratio}, std_ratio={std_ratio}"
    
    return {
        "metric_name": "ratio",
        "metric_value": float(mean_ratio),
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean_ratio = sum(results) / len(results)
    std_ratio = (sum((x - mean_ratio) ** 2 for x in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if Fraction(r, 1.2) <= 1 and abs(Fraction(r, 1) - Fraction(r, 1.2)) <= 0.1) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(result["conjecture_holds"] is False for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_ratio={result['metric_value']}, std_ratio={std_ratio}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")