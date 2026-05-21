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

def factorial(n):
    if n == 0:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def perm_to_id(perm):
    return tuple(perm)

def id_to_perm(id):
    n = len(id)
    perm = [0] * n
    used = [False] * n
    for i in range(n):
        j = 0
        k = 0
        while True:
            if not used[j]:
                if k == id[i]:
                    perm[i] = j
                    used[j] = True
                    break
                k += 1
            j += 1
    return tuple(perm)

def sign_of_permutation(perm):
    n = len(perm)
    inversions = 0
    for i in range(n):
        for j in range(i + 1, n):
            if perm[i] > perm[j]:
                inversions += 1
    return (-1) ** inversions

def matching_coefficient(matrix, g):
    n = len(matrix)
    coeff = [0] * factorial(n)
    for perm in itertools.permutations(range(n)):
        sign = sign_of_permutation(perm)
        value = g(perm)
        coeff[perm_to_id(perm)] += sign * value
    return coeff

def permanent(matrix):
    n = len(matrix)
    if n == 0:
        return 1
    if n == 1:
        return matrix[0][0]
    result = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
        sign = (-1) ** j
        result += sign * matrix[0][j] * permanent(submatrix)
    return result

def projection_on_irrep(matrix, lambda_partition):
    n = len(matrix)
    f_lambda = Fraction(factorial(n), factorial(lambda_partition))
    coeff = matching_coefficient(matrix, lambda perm: 1)
    result = [0] * factorial(n)
    for sigma in itertools.permutations(range(n)):
        id_sigma = perm_to_id(sigma)
        sum_g_chi = 0
        for g in itertools.permutations(range(n)):
            id_g = perm_to_id(g)
            chi_lambda_g = 1 if lambda_partition == [1] * n else 0
            sum_g_chi += coeff[id_g] * chi_lambda_g
        result[id_sigma] = f_lambda ** 2 * abs(sum_g_chi) ** 2 / (f_lambda ** 2 * sum(coeff))
    return result

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def identity_matrix(n):
        return [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    
    def perm_n(x):
        n = len(x)
        return sum([x[i][i] for i in range(n)])
    
    def det_n(x):
        return permanent(x)
    
    def random_invertible_matrix(n, values):
        while True:
            matrix = [[random.choice(values) for _ in range(n)] for _ in range(n)]
            if determinant(matrix) != 0:
                return matrix
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            sign = (-1) ** j
            det += sign * matrix[0][j] * determinant(submatrix)
        return det
    
    n_values = [4, 5]
    results = []
    
    for n in n_values:
        rho_perm_n = sum(projection_on_irrep(identity_matrix(n), lambda_partition=[1]*n) > 1e-9 for lambda_partition in partitions(n)) / len(partitions(n))
        rho_det_n = sum(projection_on_irrep(identity_matrix(n), lambda_partition=[n]) > 1e-9 for lambda_partition in partitions(n)) / len(partitions(n))
        
        if rho_perm_n != 1 or rho_det_n != 1:
            return {
                "metric_name": "rho",
                "metric_value": None,
                "instances_tested": n_values.count(n),
                "conjecture_holds": False,
                "counterexample": f"Sanity check failed for n={n}: rho(perm_{n})={rho_perm_n}, rho(det_{n})={rho_det_n}"
            }
        
        results.append((n, rho_perm_n, rho_det_n))
    
    for n in n_values:
        for _ in range(30):
            L = random_invertible_matrix(n * n, [-1, 0, 1])
            perm_coeff = matching_coefficient(identity_matrix(n), lambda perm: sum(L[i][j] * identity_matrix(n)[perm[i]][perm[j]] for i in range(n) for j in range(n)))
            det_coeff = matching_coefficient(identity_matrix(n), lambda perm: sum(L[i][j] * identity_matrix(n)[perm[i]][perm[j]] for i in range(n) for j in range(n)))
            
            rho_perm_n_L = sum(projection_on_irrep(perm_coeff, lambda_partition) > 1e-9 for lambda_partition in partitions(n)) / len(partitions(n))
            rho_det_n_L = sum(projection_on_irrep(det_coeff, lambda_partition) > 1e-9 for lambda_partition in partitions(n)) / len(partitions(n))
            
            if rho_perm_n_L <= rho_det_n_L:
                return {
                    "metric_name": "rho",
                    "metric_value": None,
                    "instances_tested": n_values.count(n),
                    "conjecture_holds": False,
                    "counterexample": f"Counterexample found for n={n}: rho(perm_{n}(L))={rho_perm_n_L}, rho(det_{n}(L))={rho_det_n_L}"
                }
    
    mean_rho = sum(rho_perm_n + rho_det_n for _, rho_perm_n, rho_det_n in results) / (len(results) * 2)
    std_rho = math.sqrt(sum((rho_perm_n + rho_det_n - mean_rho) ** 2 for _, rho_perm_n, rho_det_n in results) / (len(results) * 2))
    
    support_fraction = sum(rho_perm_n > rho_det_n for _, rho_perm_n, rho_det_n in results) / len(results)
    
    return {
        "metric_name": "rho",
        "metric_value": mean_rho,
        "instances_tested": n_values.count(n),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

def partitions(n):
    result = []
    def partition(n, k):
        if n == 0:
            result.append(k)
            return
        for i in range(1, n + 1):
            partition(n - i, k + [i])
    partition(n, [])
    return result

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rho = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_rho = math.sqrt(sum((r["metric_value"] - mean_rho) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='<desc>' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")