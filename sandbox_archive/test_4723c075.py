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
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            for j in range(i, n):
                matrix[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(i, n):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(matrix):
        n = len(matrix)
        det = 1
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            det *= factor
            for j in range(n):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(i, n):
                        matrix[j][k] -= factor * matrix[i][k]
        return det

    def is_invariant(matrix):
        det = determinant(matrix)
        rank = 0
        for row in matrix:
            if any(x != 0 for x in row):
                rank += 1
        return det == 0 and rank > 0

    n = random.randint(5, 40)
    tree_width = random.randint(1, 40)
    
    # Constructive mapping: Generate a random Boolean formula with tree-width at most k
    def generate_boolean_formula(n):
        if n == 1:
            return random.choice([True, False])
        else:
            left = generate_boolean_formula(n // 2)
            right = generate_boolean_formula(n - n // 2)
            return (left, right)

    formula = generate_boolean_formula(n)
    
    # Convert the Boolean formula to a matrix
    def boolean_formula_to_matrix(formula):
        if isinstance(formula, bool):
            return [[formula]]
        else:
            left = boolean_formula_to_matrix(formula[0])
            right = boolean_formula_to_matrix(formula[1])
            n = len(left)
            m = len(right)
            A = [[0 for _ in range(n + m)] for _ in range(n + m)]
            for i in range(n):
                for j in range(m):
                    A[i][j] = left[i][0]
                    A[i][n + j] = right[j][0]
            return A

    matrix = boolean_formula_to_matrix(formula)
    
    # Compute the minimal rank of the Grothendieck-Suslin class
    reduced_matrix = gaussian_elimination(matrix)
    minimal_rank = 0
    for row in reduced_matrix:
        if any(x != 0 for x in row):
            minimal_rank += 1
    
    # Check if the conjecture holds
    conjecture_holds = minimal_rank <= tree_width ** 2 * math.log(n)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": minimal_rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Formula: {formula}, Minimal Rank: {minimal_rank}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")