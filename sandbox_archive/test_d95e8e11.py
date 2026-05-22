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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_polynomial(n):
        coefficients = [random.randint(-10, 10) for _ in range(n+1)]
        return coefficients
    
    def evaluate_polynomial(poly, x):
        return sum(coeff * (x ** i) for i, coeff in enumerate(poly))
    
    def schur_representation(poly):
        n = len(poly) - 1
        representation = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            for j in range(n + 1):
                if i >= j:
                    representation[i][j] = poly[j]
        return representation
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for col in range(n):
            pivot_row = -1
            for row in range(m):
                if matrix[row][col] != 0:
                    pivot_row = row
                    break
            if pivot_row == -1:
                continue
            rank += 1
            for other_col in range(n):
                if other_col != col and matrix[pivot_row][other_col] != 0:
                    factor = matrix[pivot_row][other_col] / matrix[pivot_row][col]
                    for row in range(m):
                        matrix[row][other_col] -= factor * matrix[row][col]
        return rank
    
    def monotone_circuit_complexity(poly):
        n = len(poly) - 1
        complexity = 0
        for i in range(n + 1):
            if poly[i] != 0:
                complexity += 1
        return complexity
    
    def find_counterexample(poly):
        x_values = [i / 10.0 for i in range(-10, 11)]
        min_rank = float('inf')
        max_complexity = 0
        for x in x_values:
            representation = schur_representation(evaluate_polynomial(poly, x))
            rank = matrix_rank(representation)
            complexity = monotone_circuit_complexity(evaluate_polynomial(poly, x))
            if rank < min_rank:
                min_rank = rank
            if complexity > max_complexity:
                max_complexity = complexity
        return min_rank, max_complexity
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        poly = generate_polynomial(n)
        min_rank, max_complexity = find_counterexample(poly)
        if min_rank < max_complexity * Fraction(1, 10):
            return {
                "metric_name": "minimal_rank",
                "metric_value": min_rank,
                "instances_tested": len(x_values),
                "conjecture_holds": False,
                "counterexample": f"Polynomial: {poly}, Minimal Rank: {min_rank}, Max Complexity: {max_complexity}"
            }
        results.append((min_rank, max_complexity))
    
    mean_rank = sum(rank for rank, _ in results) / len(results)
    mean_complexity = sum(complexity for _, complexity in results) / len(results)
    support_fraction = Fraction(len([r for r, c in results if r >= c * Fraction(1, 10)]), len(results))
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": len(x_values) * len(n_values),
        "conjecture_holds": support_fraction == 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*37, 2))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = (sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = Fraction(sum(1 for r in results if r["conjecture_holds"]), len(results))
    
    if support_fraction == 1:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= Fraction(4, 5):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")