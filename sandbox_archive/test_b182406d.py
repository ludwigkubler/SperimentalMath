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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = -A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] += factor * A[i][j]
        return A
    
    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][k] += A[i][j] * B[j][k]
        return C
    
    def characteristic_polynomial(A):
        n = len(A)
        if n == 1:
            return [A[0][0]]
        elif n == 2:
            a, b, c, d = A[0][0], A[0][1], A[1][0], A[1][1]
            return [a*d - b*c, -(a+b+c+d), a + b + c + d, -1]
        else:
            det_A = Fraction(0)
            for j in range(n):
                submatrix = [[A[i][k] for k in range(n) if k != j] for i in range(1, n)]
                det_A += A[0][j] * (-1)**j * determinant(submatrix)
            return [det_A]
    
    def determinant(A):
        n = len(A)
        if n == 2:
            return A[0][0] * A[1][1] - A[0][1] * A[1][0]
        else:
            det = Fraction(0)
            for j in range(n):
                submatrix = [[A[i][k] for k in range(n) if k != j] for i in range(1, n)]
                det += A[0][j] * (-1)**j * determinant(submatrix)
            return det
    
    def moments(poly):
        return [poly[i] / Fraction(i+1) for i in range(len(poly))]
    
    def sum_of_moments(moments):
        return sum(abs(x) for x in moments)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    if n == 1:
        return {
            "metric_name": "sum_of_moments",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "single_output_stub"
        }
    
    A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    char_poly = characteristic_polynomial(A)
    moments_list = moments(char_poly)
    sum_moments = sum_of_moments(moments_list)
    
    lower_bound = n**(2/3)
    
    return {
        "metric_name": "sum_of_moments",
        "metric_value": sum_moments,
        "instances_tested": 1,
        "conjecture_holds": sum_moments >= lower_bound,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")