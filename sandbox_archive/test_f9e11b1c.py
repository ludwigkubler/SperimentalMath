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

def identity_matrix(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

def matching_coefficient(X, g):
    n = len(X)
    coeff = [0] * math.factorial(n)
    sign = 1
    def permute(matrix, perm):
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                result[i][j] = matrix[perm[i]][perm[j]]
        return result
    
    def determinant(matrix):
        if len(matrix) == 1:
            return matrix[0][0]
        det = 0
        sign = 1
        for i in range(len(matrix)):
            submatrix = [row[:i] + row[i+1:] for row in matrix[1:]]
            det += sign * matrix[0][i] * determinant(submatrix)
            sign *= -1
        return det
    
    def perm_to_id(perm):
        id_perm = [0] * n
        for i, val in enumerate(perm):
            id_perm[val] = i
        return tuple(id_perm)
    
    def sign_of_permutation(perm):
        inversions = 0
        for i in range(n):
            for j in range(i + 1, n):
                if perm[i] > perm[j]:
                    inversions += 1
        return (-1) ** inversions
    
    for perm in itertools.permutations(range(n)):
        sign = sign_of_permutation(perm)
        coeff[perm_to_id(perm)] += sign * g(perm)
    
    return coeff

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [4, 5]
    results = []
    
    for n in n_values:
        perm_coeff = matching_coefficient(identity_matrix(n), lambda perm: 1)
        det_coeff = matching_coefficient(identity_matrix(n), lambda perm: (-1)**sum(perm))
        
        if sum(abs(x) ** 2 for x in perm_coeff) != len(perm_coeff):
            return {
                "metric_name": "rho",
                "metric_value": None,
                "instances_tested": 0,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        if sum(abs(x) ** 2 for x in det_coeff) != len(det_coeff):
            return {
                "metric_name": "rho",
                "metric_value": None,
                "instances_tested": 0,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        rho_perm = sum(1 for x in perm_coeff if abs(x) ** 2 > 1e-9)
        rho_det = sum(1 for x in det_coeff if abs(x) ** 2 > 1e-9)
        
        results.append((rho_perm, rho_det))
    
    total_rho_perm = sum(rho[0] for rho in results)
    total_rho_det = sum(rho[1] for rho in results)
    avg_rho_perm = total_rho_perm / len(results)
    avg_rho_det = total_rho_det / len(results)
    
    support_count = sum(1 for rho in results if rho[0] >= rho[1] + 1)
    support_fraction = support_count / len(results)
    
    return {
        "metric_name": "rho",
        "metric_value": avg_rho_perm,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 25/30,
        "counterexample": "" if support_fraction >= 25/30 else f"n=4 or n=5 failed with rho(perm) <= rho(det)"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    avg_rho_perm = sum(r['metric_value'] for r in results) / len(results)
    avg_rho_det = sum(r['instances_tested'] * (r['metric_value'] if r['conjecture_holds'] else 0) for r in results) / sum(r['instances_tested'] for r in results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_rho_perm} std=0 support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"n=4 or n=5 failed with rho(perm) <= rho(det)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=budget_exceeded n_tested=30")