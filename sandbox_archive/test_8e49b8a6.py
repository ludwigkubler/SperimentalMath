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

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gram_schmidt(monomials):
        n = len(monomials)
        Q = []
        for i in range(n):
            q_i = monomials[i]
            for j in range(i):
                q_j = Q[j]
                projection = sum(q_i[k] * q_j[k] for k in range(len(q_i))) / sum(q_j[k] ** 2 for k in range(len(q_j)))
                q_i = [q_i[k] - projection * q_j[k] for k in range(len(q_i))]
            Q.append(q_i)
        return Q
    
    def degree_d_sos_moment_matrix(n, d):
        monomials = [[1 if i == j else 0 for j in range(d+1)] for i in range(n)]
        Q = gram_schmidt(monomials)
        matrix = [[sum(Q[i][k] * Q[j][l] for k in range(len(Q[i])) for l in range(len(Q[j]))) for j in range(n)] for i in range(n)]
        return matrix
    
    def eigenvalues(matrix):
        n = len(matrix)
        if n == 1:
            return [matrix[0][0]]
        if n == 2:
            a, b, c, d = matrix[0][0], matrix[0][1], matrix[1][0], matrix[1][1]
            trace = a + d
            det = a * d - b * c
            return [trace / 2 + math.sqrt(trace ** 2 / 4 - det), trace / 2 - math.sqrt(trace ** 2 / 4 - det)]
        p = sum(matrix[i][i] for i in range(n))
        q = sum(sum(matrix[i][j] * matrix[j][i] for j in range(i+1, n)) for i in range(n))
        r = sum(sum(sum(matrix[i][k] * matrix[k][l] * matrix[l][j] for k in range(i+1, l)) for l in range(j+1, n)) for i in range(n) for j in range(i+1, n))
        A = [[p - matrix[i][i], q - sum(matrix[i][j] for j in range(i+1, n)), r - sum(sum(matrix[i][k] * matrix[k][l] for k in range(i+1, l)) for l in range(j+1, n))] for i in range(n)]
        B = [[p - matrix[j][j], q - sum(matrix[j][i] for i in range(j+1, n)), r - sum(sum(matrix[j][k] * matrix[k][l] for k in range(j+1, l)) for l in range(i+1, n))] for j in range(n)]
        C = [[p - matrix[i][i], q - sum(matrix[i][j] for j in range(i+1, n)), r - sum(sum(matrix[i][k] * matrix[k][l] for k in range(i+1, l)) for l in range(j+1, n))] for i in range(n)]
        D = [[p - matrix[j][j], q - sum(matrix[j][i] for i in range(j+1, n)), r - sum(sum(matrix[j][k] * matrix[k][l] for k in range(j+1, l)) for l in range(i+1, n))] for j in range(n)]
        eigenvals_A = eigenvalues(A)
        eigenvals_B = eigenvalues(B)
        eigenvals_C = eigenvalues(C)
        eigenvals_D = eigenvalues(D)
        return eigenvals_A + eigenvals_B + eigenvals_C + eigenvals_D
    
    def goemans_williamson_ratio(n):
        # Placeholder for actual Goemans-Williamson ratio calculation
        return random.random()
    
    n = 40
    d = 2
    matrix = degree_d_sos_moment_matrix(n, d)
    eigenvals = eigenvalues(matrix)
    sum_abs_eigenvals = sum(abs(e) for e in eigenvals)
    goemans_williamson = goemans_williamson_ratio(n)
    
    metric_name = "Sum of Absolute Eigenvalues"
    metric_value = sum_abs_eigenvals
    instances_tested = 1
    conjecture_holds = abs(sum_abs_eigenvals - n ** d * math.log(n)) < 0.1 * n ** d * math.log(n)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")