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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def identity_matrix(n):
        return [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    
    def permute(matrix, perm):
        n = len(matrix)
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                result[i][j] = matrix[perm[i]][perm[j]]
        return result
    
    def matching_coefficient(X, g):
        n = len(X)
        coeff = [0] * math.factorial(n)
        for perm in itertools.permutations(range(n)):
            sign = 1
            val = X[perm[0]][perm[0]]
            for i in range(1, n):
                sign *= (-1) ** (perm[i-1] > perm[i])
                val *= X[perm[i-1]][perm[i]]
            coeff[id(perm)] += sign * val
        return coeff
    
    def permanent(matrix):
        n = len(matrix)
        if n == 0:
            return 1
        elif n == 1:
            return matrix[0][0]
        else:
            det = 0
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
                det += ((-1) ** j) * matrix[0][j] * permanent(submatrix)
            return det
    
    def project_onto_lambda(c, λ):
        n = len(c)
        f_lambda = Fraction(1, math.factorial(len(λ)))
        result = 0
        for τ in itertools.permutations(range(n)):
            sum_g = 0
            for g in itertools.permutations(range(n)):
                sum_g += c[id(g)] * (g[τ.index(i)] for i in range(n))
            result += abs(sum_g) ** 2
        return f_lambda ** 2 * result
    
    def specht_block_count(c):
        n = len(c)
        λs = partitions(n)
        count = sum(project_onto_lambda(c, λ) > 1e-9 for λ in λs)
        return count
    
    def partitions(n):
        if n == 0:
            return [[]]
        result = []
        for p in partitions(n - 1):
            for i in range(len(p) + 1):
                new_partition = p[:i] + [p[i] + 1] + p[i+1:]
                if new_partition not in result:
                    result.append(new_partition)
        return result
    
    def random_invertible_matrix(n, values):
        while True:
            matrix = [[random.choice(values) for _ in range(n)] for _ in range(n)]
            det = permanent(matrix)
            if det != 0:
                return matrix
    
    n_values = [4, 5]
    results = []
    
    for n in n_values:
        perm_coeff = matching_coefficient(identity_matrix(n), identity_matrix(n))
        det_coeff = matching_coefficient(identity_matrix(n), [[1 if i == j else -1 if i != j and (i + j) % 2 == 0 else 0 for j in range(n)] for i in range(n)])
        
        if specht_block_count(perm_coeff) != 1 or specht_block_count(det_coeff) != 1:
            return {
                "metric_name": "specht_block_count",
                "metric_value": None,
                "instances_tested": 0,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        for _ in range(30):
            L = random_invertible_matrix(n, [-1, 0, 1])
            perm_L_coeff = matching_coefficient(identity_matrix(n), permute(L, [i for i in range(n)]))
            det_L_coeff = matching_coefficient(identity_matrix(n), permute(L, [(n-1-i) % n for i in range(n)]))
            
            if specht_block_count(perm_L_coeff) <= specht_block_count(det_L_coeff):
                return {
                    "metric_name": "specht_block_count",
                    "metric_value": None,
                    "instances_tested": 0,
                    "conjecture_holds": False,
                    "counterexample": f"seed={seed}, n={n}"
                }
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for x in results if x >= 25/30) / len(results)
    
    return {
        "metric_name": "specht_block_count",
        "metric_value": mean,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        if "metric_value" in result and result["metric_value"] is not None:
            results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for x in results if x >= 0.8) / len(results)
    
    if all(x >= 0.8 for x in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(x < 0.8 for x in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result < 0.8)
        print(f"RESULT: FALSIFIED counterexample='seed={first_failing_seed}' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")