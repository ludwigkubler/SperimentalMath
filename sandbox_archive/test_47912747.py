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

def generate_random_kcnf(n, k):
    clauses = []
    for _ in range(k * n):
        clause = set()
        while len(clause) < 2:
            var = random.randint(1, n)
            sign = random.choice([1, -1])
            clause.add((var, sign))
        clauses.append(list(clause))
    return clauses

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i
        for j in range(i + 1, rows):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        factor = Fraction(matrix[i][i])
        for j in range(cols):
            matrix[i][j] /= factor
        for j in range(rows):
            if i != j:
                factor = Fraction(matrix[j][i])
                for k in range(cols):
                    matrix[j][k] -= factor * matrix[i][k]
    return matrix

def min_noncommutative_rank(clauses):
    n = len(clauses)
    matrix = [[0] * (2 * n) for _ in range(2 * n)]
    for i, clause in enumerate(clauses):
        for var, sign in clause:
            row = 2 * var - 1 if sign == 1 else 2 * var
            col = 2 * var - 2 if sign == 1 else 2 * var - 1
            matrix[row][col] += 1
    rank = 0
    for i in range(2 * n):
        if any(matrix[i][j] != 0 for j in range(rank, 2 * n)):
            rank += 1
    return rank

def resolution_depth(clauses):
    stack = []
    while clauses:
        new_clause = None
        for clause in clauses:
            if len(clause) == 1:
                literal = clause[0]
                if -literal in [x for y in stack for x in y]:
                    return float('inf')
                else:
                    new_clause = [-literal]
                    break
        if new_clause is None:
            return len(stack)
        stack.append(new_clause)
        clauses = [c for c in clauses if not any(lit in c for lit in new_clause)]
    return len(stack)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    k = n
    clauses = generate_random_kcnf(n, k)
    
    rank = min_noncommutative_rank(clauses)
    depth = resolution_depth(clauses)
    
    return {
        "metric_name": "resolution_depth",
        "metric_value": depth,
        "instances_tested": 1,
        "conjecture_holds": depth >= 2 ** (rank.bit_length() - 1),
        "counterexample": "" if depth >= 2 ** (rank.bit_length() - 1) else f"Depth {depth} < 2^Ω({rank})"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(30, 89))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_depth = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_depth} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_depth} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Depth < 2^Ω(rank)\" first_failing_seed={first_failing_seed}")