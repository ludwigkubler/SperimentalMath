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
    
    def xor_and_tree_width(f):
        n = len(f)
        if n == 1:
            return 0
        mid = n // 2
        left_width = xor_and_tree_width(f[:mid])
        right_width = xor_and_tree_width(f[mid:])
        return max(left_width, right_width) + 1
    
    def frobenius_norm(matrix):
        n = len(matrix)
        sum_of_squares = 0
        for i in range(n):
            for j in range(n):
                sum_of_squares += matrix[i][j] ** 2
        return math.sqrt(sum_of_squares)
    
    def characteristic_polynomial(f):
        n = len(f)
        if n == 1:
            return [[f[0], -1]]
        mid = n // 2
        left_poly = characteristic_polynomial(f[:mid])
        right_poly = characteristic_polynomial(f[mid:])
        
        result = []
        for i in range(len(left_poly)):
            for j in range(len(right_poly)):
                coeff = left_poly[i][0] * right_poly[j][0]
                x_term = left_poly[i][1] + right_poly[j][1]
                if len(result) == 0 or result[-1][1] != x_term:
                    result.append([coeff, x_term])
                else:
                    result[-1][0] += coeff
        return result
    
    def matrix_from_polynomial(poly):
        n = len(poly)
        matrix = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            matrix[i][i] = poly[i][0]
        for i in range(n - 1):
            for j in range(i + 1, n):
                matrix[j][i] = poly[j - i - 1][0] * (-poly[0][1]) ** (j - i - 1)
                matrix[i][j] = matrix[j][i]
        return matrix
    
    def min_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if all(matrix[j][i] == 0 for j in range(i, n)):
                continue
            pivot_row = i
            while matrix[pivot_row][i] == 0:
                pivot_row += 1
                if pivot_row == n:
                    return rank
            for j in range(n):
                if j != i:
                    factor = matrix[j][i] / matrix[pivot_row][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[pivot_row][k]
            rank += 1
        return rank
    
    def log_n(f, n):
        while f > 1 and n > 0:
            f = math.log(f)
            n -= 1
        return f
    
    def log_w(w, w):
        while w > 1 and w > 0:
            w = math.log(w)
            w -= 1
        return w
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            f = [random.randint(0, 1) for _ in range(n)]
            width = xor_and_tree_width(f)
            poly = characteristic_polynomial(f)
            matrix = matrix_from_polynomial(poly)
            rank = min_rank(matrix)
            
            total_rank += rank
            instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    conjecture_holds = mean_rank <= 2 * width ** (1/3) * log_w(width, width)
    
    return {
        "metric_name": "Minimal Rank of Frobenius Norm",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Mean rank {mean_rank} exceeds 2 * width^(1/3) * log^width(f)"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Mean rank exceeds 2 * width^(1/3) * log^width(f)\" first_failing_seed={first_failing_seed}")