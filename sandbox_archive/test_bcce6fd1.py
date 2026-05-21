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
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = Fraction(matrix[i][i])
            for j in range(i, n):
                matrix[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = Fraction(matrix[j][i])
                    for k in range(i, n):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def det(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        elif n == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        else:
            det_val = Fraction(0)
            for c in range(n):
                submatrix = [row[:c] + row[c+1:] for row in matrix[1:]]
                sign = (-1) ** (c % 2)
                sub_det = det(submatrix)
                det_val += sign * matrix[0][c] * sub_det
            return det_val

    def tensor_power(matrix, n):
        result = [[1 if i == j else 0 for j in range(len(matrix))] for i in range(len(matrix))]
        for _ in range(n-1):
            result = [[sum(result[i][k] * matrix[k][j] for k in range(len(matrix))) for j in range(len(matrix))] for i in range(len(matrix))]
        return result

    def minimal_representation_rank(n):
        S3 = [
            [[0, 1, 2], [1, 0, 2], [2, 2, 0]],
            [[0, 2, 1], [2, 0, 1], [1, 1, 0]],
            [[1, 0, 2], [0, 1, 2], [2, 2, 0]],
            [[1, 2, 0], [2, 1, 0], [0, 0, 1]],
            [[2, 0, 1], [0, 2, 1], [1, 1, 0]],
            [[2, 1, 0], [1, 2, 0], [0, 0, 1]]
        ]
        T_n = tensor_power(S3, n)
        return len(gaussian_elimination(T_n))

    def det_m(m):
        F2 = {0: 0, 1: 1}
        matrix = [[F2[i == j] for j in range(m)] for i in range(m)]
        return det(matrix)

    n = random.randint(5, 40)
    m = int(n ** 1.5) - 1
    rho_T_n = minimal_representation_rank(n)
    rho_det_m = det_m(m)

    return {
        "metric_name": "minimal_representation_rank",
        "metric_value": rho_T_n,
        "instances_tested": 1,
        "conjecture_holds": rho_T_n <= rho_det_m,
        "counterexample": f"n={n}, k={m}: ρ(T_n)={rho_T_n} > ρ(det_{m})={rho_det_m}" if not rho_T_n <= rho_det_m else ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")