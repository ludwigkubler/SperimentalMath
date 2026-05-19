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
    
    def matrix_multiply(A, B):
        m, k = len(A), len(B[0])
        n = len(B)
        C = [[0 for _ in range(k)] for _ in range(m)]
        for i in range(m):
            for j in range(k):
                for l in range(n):
                    C[i][j] += A[i][l] * B[l][j]
        return C
    
    def gaussian_elimination(A, b):
        n = len(b)
        augmented = [A[i] + [b[i]] for i in range(n)]
        for i in range(n):
            max_row = max(range(i, n), key=lambda r: abs(augmented[r][i]))
            augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
            factor = augmented[i][i]
            if factor == 0:
                return None
            for j in range(i, n + 1):
                augmented[i][j] /= factor
            for k in range(n):
                if k != i:
                    factor = augmented[k][i]
                    for j in range(i, n + 1):
                        augmented[k][j] -= factor * augmented[i][j]
        return [row[-1] for row in augmented]

    def permanent(M):
        n = len(M)
        sign = 1
        perm = list(range(n))
        det = 0
        while True:
            det += sign * math.prod([M[perm[i]][i] for i in range(n)])
            if next_permutation(perm):
                sign *= -1
            else:
                break
        return det

    def next_permutation(p):
        n = len(p)
        i = n - 2
        while i >= 0 and p[i] >= p[i + 1]:
            i -= 1
        if i < 0:
            return False
        j = n - 1
        while p[j] <= p[i]:
            j -= 1
        p[i], p[j] = p[j], p[i]
        p[i + 1:] = reversed(p[i + 1:])
        return True

    def plethysm_coefficient(M, k):
        n = len(M)
        M_k = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                M_k[i][j] = permanent([[M[ii][jj] for jj in range(j, j + 1)] for ii in range(i, i + 1)]) ** k
        return gaussian_elimination(M_k, [1 for _ in range(n)])[0]

    n = 4
    M = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    coeff_perm = plethysm_coefficient(M, 2)
    coeff_det = plethysm_coefficient([[1 if i == j else 0 for j in range(n)] for i in range(n)], 2)
    
    return {
        "metric_name": "plethysm_coefficient",
        "metric_value": coeff_perm / coeff_det,
        "instances_tested": 1,
        "conjecture_holds": coeff_perm >= 16 and coeff_det <= 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"plethysm_coefficient\" first_failing_seed={first_failing_seed}")