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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
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
                if j != i:
                    factor = Fraction(matrix[j][i])
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def matrix_rank(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for i in range(min(rows, cols)):
            if all(abs(matrix[j][i]) == 0 for j in range(rank)):
                break
            rank += 1
        return rank

    def tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n + 1)]
        clauses = []
        for i in range(1, n + 1):
            clauses.append([variables[i - 1]])
        for i in range(2, n + 1):
            clauses.append([-variables[i - 2], variables[i - 1]])
        return variables, clauses

    def monomial_ideal(variables, clauses):
        ideal = set()
        for clause in clauses:
            product = 1
            for var in clause:
                if var.startswith('x'):
                    product *= int(var[1:])
                else:
                    product *= -int(var[1:])
            ideal.add(product)
        return sorted(ideal)

    def associated_graded_ring(ideal):
        n = len(ideal)
        graded_ring = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(i, n):
                if ideal[i] % ideal[j] == 0:
                    graded_ring[i][j] = 1
        return graded_ring

    def resolution_width(clauses):
        stack = []
        width = 0
        for clause in clauses:
            new_clause = [var for var in clause if var not in stack]
            if not new_clause:
                continue
            stack.extend(new_clause)
            width = max(width, len(stack))
        return width

    n = random.randint(5, 40)
    variables, clauses = tseitin_formula(n)
    ideal = monomial_ideal(variables, clauses)
    graded_ring = associated_graded_ring(ideal)
    rank = matrix_rank(gaussian_elimination(graded_ring))

    resolution_width_val = resolution_width(clauses)

    return {
        "metric_name": "resolution_width",
        "metric_value": resolution_width_val,
        "instances_tested": 1,
        "conjecture_holds": resolution_width_val >= 2**(n/2),
        "counterexample": "" if resolution_width_val >= 2**(n/2) else f"Width {resolution_width_val} < 2^{(n/2)}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")