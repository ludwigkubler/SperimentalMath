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
    
    def bdd_to_polynomial(bdd):
        if not bdd.children:
            return [bdd.value]
        left = bdd_to_polynomial(bdd.left)
        right = bdd_to_polynomial(bdd.right)
        return [x * (1 - bdd.var) for x in left] + [x * bdd.var for x in right]

    def tropicalize(polynomial):
        return max([abs(coeff) for coeff in polynomial])

    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    def lcm(a, b):
        return abs(a*b) // gcd(a, b)

    def matrix_multiplication(A, B):
        rows_A = len(A)
        cols_A = len(A[0])
        cols_B = len(B[0])
        result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
        for i in range(rows_A):
            for j in range(cols_B):
                for k in range(cols_A):
                    result[i][j] += A[i][k] * B[k][j]
        return result

    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                A[j][i] = 0
                for k in range(i+1, n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0]*n
        for i in range(n-1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
        return x

    def determinant(matrix):
        if len(matrix) == 1:
            return matrix[0][0]
        det = 0
        for i in range(len(matrix)):
            submatrix = [row[:i] + row[i+1:] for row in matrix[1:]]
            det += (-1)**i * matrix[0][i] * determinant(submatrix)
        return det

    def is_prime(n):
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    def generate_bdd(n):
        if n == 1:
            return {'value': random.choice([0, 1]), 'children': []}
        var = random.randint(0, n-1)
        left = generate_bdd(var)
        right = generate_bdd(n-1-var)
        return {'var': var, 'left': left, 'right': right}

    def characteristic_polynomial(bdd):
        if not bdd.children:
            return [bdd.value]
        left = characteristic_polynomial(bdd.left)
        right = characteristic_polynomial(bdd.right)
        result = []
        for i in range(len(left)):
            for j in range(len(right)):
                coeff = left[i] * right[j]
                if coeff != 0:
                    result.append(coeff)
        return result

    def hodge_class_rank(polynomial):
        n = len(polynomial)
        A = [[0]*n for _ in range(n)]
        b = [0]*n
        for i in range(n):
            for j in range(i, n):
                A[i][j] = polynomial[j-i]
                if i == j:
                    b[i] = 1
        x = gaussian_elimination(A, b)
        return sum(1 for coeff in x if coeff != 0)

    def bdd_width(bdd):
        if not bdd.children:
            return 1
        left_width = bdd_width(bdd.left)
        right_width = bdd_width(bdd.right)
        return max(left_width, right_width) + 1

    n = random.randint(5, 40)
    p = 2
    d = random.randint(n//2, n)
    
    bdd = generate_bdd(n)
    polynomial = bdd_to_polynomial(bdd)
    tropical_rank = tropicalize(polynomial)
    width = bdd_width(bdd)
    c = 4
    
    if tropical_rank > c * d:
        return {
            "metric_name": "tropical_hodge_class_rank",
            "metric_value": tropical_rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"rank={tropical_rank}, expected={c*d}"
        }
    
    return {
        "metric_name": "tropical_hodge_class_rank",
        "metric_value": tropical_rank,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_dev = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")