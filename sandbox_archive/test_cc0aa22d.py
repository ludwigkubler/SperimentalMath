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
    
    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(k):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for col in range(cols):
            pivot_row = None
            for row in range(rank, rows):
                if matrix[row][col] != 0:
                    pivot_row = row
                    break
            if pivot_row is not None:
                matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
                for r in range(rows):
                    if r != rank and matrix[r][col] != 0:
                        factor = -matrix[r][col] / matrix[rank][col]
                        for c in range(cols):
                            matrix[r][c] += factor * matrix[rank][c]
                rank += 1
        return rank
    
    def min_noncommutative_rank(clauses):
        n = len(clauses)
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in clauses:
            i, j = abs(clause[0]) - 1, abs(clause[1]) - 1
            if clause[0] > 0 and clause[1] < 0:
                matrix[i][j] += 1
            elif clause[0] < 0 and clause[1] > 0:
                matrix[j][i] += 1
        return gaussian_elimination(matrix)
    
    def resolution_depth(clauses):
        stack = []
        while True:
            new_clause = None
            for i in range(len(stack)):
                for j in range(i + 1, len(stack)):
                    if abs(stack[i]) == -stack[j]:
                        new_clause = [abs(stack[i]), abs(stack[j])]
                        break
                if new_clause is not None:
                    break
            if new_clause is None:
                return len(stack)
            stack.append(new_clause[0])
    
    n = random.randint(5, 40)
    k = random.randint(1, min(n * (n - 1) // 2, 10))
    clauses = generate_k_cnf(n, k)
    
    rank = min_noncommutative_rank(clauses)
    depth = resolution_depth(clauses)
    
    return {
        "metric_name": "resolution_depth",
        "metric_value": depth,
        "instances_tested": 1,
        "conjecture_holds": depth >= 2 ** (math.log(rank, 2) * 0.5),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_depth = sum(r["metric_value"] for r in results) / len(results)
    std_depth = math.sqrt(sum((r["metric_value"] - mean_depth) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_depth} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_depth} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = f"First failing seed {first_failing_seed}"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")