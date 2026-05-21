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
    n = 16
    random.seed(seed)
    
    def generate_read_twice_bp(n):
        bp = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j or (i + j) % 2 == 0:
                    bp[i][j] = 1 / (n - 1)
                else:
                    bp[i][j] = 0
        return bp
    
    def matrix_multiplication(A, B):
        result = [[sum(a * b for a, b in zip(row_i, col_j)) for col_j in zip(*B)] for row_i in A]
        return result
    
    def determinant(matrix):
        if len(matrix) == 1:
            return matrix[0][0]
        det = Fraction(0)
        for j in range(len(matrix)):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** j * matrix[0][j] * determinant(submatrix)
        return det
    
    def tensor_product(matrices):
        result = matrices[0]
        for matrix in matrices[1:]:
            result = [[sum(a * b for a, b in zip(row_i, col_j)) for col_j in zip(*matrix)] for row_i in result]
        return result
    
    P = generate_read_twice_bp(n)
    M = [P] + [matrix_multiplication(P, P) for _ in range(1, n)]
    
    det_sum = sum(determinant(M[i]) for i in range(n))
    rho = - (1/n) * math.log(det_sum)
    
    return {
        "metric_name": "free_entropy",
        "metric_value": rho,
        "instances_tested": 1,
        "conjecture_holds": rho >= 0.3 * math.log(n),
        "counterexample": "" if rho >= 0.3 * math.log(n) else "rho < 0.3 log n"
    }

if __name__ == "__main__":
    seeds = [int(seed) for seed in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rho = sum(r["metric_value"] for r in results) / len(results)
    std_rho = math.sqrt(sum((r["metric_value"] - mean_rho) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rho < 0.3 log n\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")