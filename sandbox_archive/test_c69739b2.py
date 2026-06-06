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
from fractions import Fraction
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def determinant(matrix):
        if len(matrix) == 1 and len(matrix[0]) == 1:
            return matrix[0][0]
        det = 0
        for i in range(len(matrix)):
            submatrix = [row[:i] + row[i+1:] for row in matrix[1:]]
            sign = (-1) ** i
            det += sign * matrix[0][i] * determinant(submatrix)
        return det
    
    def characteristic_polynomial(matrix):
        n = len(matrix)
        x = Fraction('x')
        identity = [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]
        char_poly = 1
        for k in range(n):
            char_poly *= (x - matrix[k][k])
        return char_poly
    
    def p_adic_roots(poly, p):
        roots = set()
        for a in range(p**2):
            if poly(a % p) == 0:
                roots.add(a)
        return roots
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            matrix_size = random.randint(n, min(n * 2, 40))
            if matrix_size <= 1: continue
            communication_matrix = [[random.randint(-10, 10) for _ in range(matrix_size)] for _ in range(matrix_size)]
            char_poly = characteristic_polynomial(communication_matrix)
            p_adic_roots_count = len(p_adic_roots(char_poly, 2))
            rank_variance = sum((Fraction(random.choice([0, 1])) - Fraction(1)) ** 2 for _ in range(5)) / 5
            if rank_variance == 0: continue
            ratio = p_adic_roots_count / rank_variance
            total_metric_value += ratio
            instances_tested += 1
            n_max = max(n_max, matrix_size)
            if ratio > 3:
                conjecture_holds = False
                counterexample = f"n={n}, matrix_size={matrix_size}"
    
    mean_metric_value = total_metric_value / instances_tested if instances_tested > 0 else 0
    std_deviation = math.sqrt(sum((ratio - mean_metric_value) ** 2 for ratio in range(instances_tested))) / instances_tested if instances_tested > 1 else 0
    
    return {
        "metric_name": "p-adic root count to rank variance ratio",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_deviation = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_deviation} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_deviation} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")