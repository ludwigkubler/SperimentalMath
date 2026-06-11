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
    
    def tseitin_formula(n, d):
        if n <= 0 or d <= 0:
            return []
        vertices = list(range(1, n + 1))
        edges = set()
        for _ in range(d):
            u = random.choice(vertices)
            v = random.choice(vertices)
            while u == v:
                v = random.choice(vertices)
            edges.add((u, v))
        return edges
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i + 1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                continue
            for j in range(i + 1, cols):
                matrix[i][j] /= matrix[i][i]
            for j in range(rows):
                if j != i and matrix[j][i] != 0:
                    factor = matrix[j][i]
                    for k in range(i, cols):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def symmetric_tensor_rank(poly):
        n = len(poly)
        tensor = [[poly[i][j] for j in range(n)] for i in range(n)]
        rank = 0
        while True:
            if not any(tensor[i][j] != 0 for i in range(rank) for j in range(rank)):
                break
            pivot_row, pivot_col = None, None
            for i in range(rank):
                for j in range(rank):
                    if tensor[i][j] != 0:
                        pivot_row, pivot_col = i, j
                        break
                if pivot_row is not None:
                    break
            if pivot_row is None:
                break
            for j in range(n):
                if j == pivot_col:
                    continue
                factor = tensor[j][pivot_col] / tensor[pivot_row][pivot_col]
                for k in range(rank):
                    tensor[j][k] -= factor * tensor[pivot_row][k]
            rank += 1
        return rank
    
    def resolution_width(formula):
        # Simplified DPLL solver to estimate width
        stack = []
        assignment = {}
        for u, v in formula:
            if u not in assignment and v not in assignment:
                assignment[u] = True
                assignment[v] = False
                stack.append((u, v))
            elif u in assignment and v not in assignment:
                assignment[v] = not assignment[u]
                stack.append((v,))
            elif u not in assignment and v in assignment:
                assignment[u] = not assignment[v]
                stack.append((u,))
            else:
                return 1
        while stack:
            clause = stack.pop()
            if len(clause) == 1:
                literal = clause[0]
                for var, val in assignment.items():
                    if var == abs(literal):
                        assignment[var] = literal > 0
                        break
                else:
                    return 1
            else:
                literal = random.choice(clause)
                for var, val in assignment.items():
                    if var == abs(literal):
                        assignment[var] = literal > 0
                        stack.append((var,))
                        break
        return len(assignment) - sum(val for _, val in assignment.items())
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_str = 0
    total_width = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            d = random.randint(1, min(n, 5))
            formula = tseitin_formula(n, d)
            poly = [random.choice([0, 1]) for _ in range(n)]
            str_rank = symmetric_tensor_rank(poly)
            width = resolution_width(formula)
            total_str += str_rank
            total_width += width
            instances_tested += 1
    
    mean_str = total_str / instances_tested
    mean_width = total_width / instances_tested
    correlation_coefficient = (instances_tested * sum(str_rank * width for str_rank, width in zip(total_str, total_width)) -
                               mean_str * total_width) / math.sqrt((instances_tested * sum(str_rank**2 for str_rank in total_str) - mean_str**2) *
                                                                   (instances_tested * sum(width**2 for width in total_width) - mean_width**2))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": "" if abs(correlation_coefficient) >= 0.8 else f"correlation_coefficient={correlation_coefficient}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if abs(r["metric_value"]) >= 0.8) / len(results)
    
    if all(abs(r["metric_value"]) >= 0.8 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result["metric_value"]) < 0.8)
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient<{result['metric_value']}>' first_failing_seed={first_failing_seed}")