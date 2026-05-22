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

def schur_representation(poly):
    n = len(poly) - 1
    representation = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        for j in range(n + 1):
            if i == j:
                representation[i][j] = poly[i]
            elif i > j:
                representation[i][j] = -poly[j]
    return representation

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        for j in range(i + 1, n):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]
    return matrix

def rank(matrix):
    n = len(matrix)
    reduced_matrix = gaussian_elimination(matrix)
    rank = 0
    for i in range(n):
        if all(reduced_matrix[i][j] == 0 for j in range(n)):
            break
        rank += 1
    return rank

def evaluate_polynomial(poly, x):
    result = 0
    for i, coeff in enumerate(poly):
        result += coeff * (x ** i)
    return result

def find_counterexample(polynomials):
    min_rank = float('inf')
    max_complexity = 0
    for poly in polynomials:
        representation = schur_representation(evaluate_polynomial(poly, random.random()))
        current_rank = rank(representation)
        if current_rank < min_rank:
            min_rank = current_rank
        complexity = len(poly) - 1
        if complexity > max_complexity:
            max_complexity = complexity
    return min_rank, max_complexity

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        polynomials = [random.random() for _ in range(random.randint(5, n))]
        min_rank, max_complexity = find_counterexample(polynomials)
        if min_rank < Fraction(n) * max_complexity:
            return {
                "metric_name": "min_rank_over_max_complexity",
                "metric_value": float('inf'),
                "instances_tested": len(polynomials),
                "conjecture_holds": False,
                "counterexample": f"n={n}, min_rank={min_rank}, max_complexity={max_complexity}"
            }
        results.append(min_rank / max_complexity)
    mean_value = sum(results) / len(results)
    std_value = (sum((x - mean_value) ** 2 for x in results) / len(results)) ** 0.5
    return {
        "metric_name": "min_rank_over_max_complexity",
        "metric_value": mean_value,
        "instances_tested": sum(len(polynomials) for n, polynomials in zip(n_values, [random.random() for _ in range(random.randint(5, n)) for n in n_values])),
        "conjecture_holds": all(x >= 1 for x in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    mean_value = sum(results) / len(results)
    std_value = (sum((x - mean_value) ** 2 for x in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r >= 1) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r < 1 for r in results):
        first_failing_seed = seeds[results.index(min(r for r in results if r < 1))]
        print(f"RESULT: FALSIFIED counterexample=\"min_rank_over_max_complexity\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")