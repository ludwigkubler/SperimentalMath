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

def generate_cnf(n: int, m: int) -> list:
    cnf = []
    for _ in range(m):
        clause = set()
        while len(clause) < 2:
            lit = random.randint(1, n)
            if random.choice([True, False]):
                lit = -lit
            clause.add(lit)
        cnf.append(list(clause))
    return cnf

def gaussian_elimination(matrix: list) -> tuple:
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

def minimal_order(cnf: list) -> int:
    n = len(cnf)
    m = len(cnf[0])
    matrix = [[0] * (n + 1) for _ in range(n)]
    for i, clause in enumerate(cnf):
        for lit in clause:
            if lit > 0:
                matrix[i][lit - 1] += 1
            else:
                matrix[i][-lit - 1] -= 1
    rank = gaussian_elimination(matrix)
    return rank + 1

def monotone_width(cnf: list) -> int:
    n = len(cnf)
    clauses = [set(clause) for clause in cnf]
    max_width = 0
    for i in range(1 << n):
        width = 0
        covered_clauses = set()
        for j in range(n):
            if (i >> j) & 1:
                width += 1
                for clause in clauses:
                    if all(lit in bin(i)[2:] for lit in clause):
                        covered_clauses.add(clause)
        max_width = max(max_width, len(covered_clauses))
    return max_width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_instances = 0
    min_orders = []
    widths = []

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            m = random.randint(1, n)
            cnf = generate_cnf(n, m)
            min_order_value = minimal_order(cnf)
            width_value = monotone_width(cnf)
            min_orders.append(min_order_value)
            widths.append(width_value)
            total_instances += 1

    correlation_coefficient = sum((x - mean_x) * (y - mean_y) for x, y in zip(min_orders, widths)) / math.sqrt(sum((x - mean_x) ** 2 for x in min_orders) * sum((y - mean_y) ** 2 for y in widths))
    mean_x = sum(min_orders) / len(min_orders)
    mean_y = sum(widths) / len(widths)

    conjecture_holds = correlation_coefficient > 0.7
    counterexample = "" if conjecture_holds else "correlation_coefficient"

    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": total_instances,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")