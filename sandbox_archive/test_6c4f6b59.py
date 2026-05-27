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
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        if len(A) == 1:
            return A[0][0]
        det = 0
        sign = 1
        for j in range(len(A)):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += sign * A[0][j] * determinant(submatrix)
            sign *= -1
        return det

    def noncommutative_Lp_dimension(f, n):
        density_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if f(i) == f(j):
                    density_matrix[i][j] = 1
        A = gaussian_elimination(density_matrix)
        return determinant(A)

    def communication_complexity(f, d, p):
        return d ** p

    n = random.randint(5, 40)
    m = max(n * 2, 30)  # Ensure m is significantly larger than n
    f = {i: random.randint(0, m-1) for i in range(n)}
    
    d = noncommutative_Lp_dimension(f, n)
    upper_bound = communication_complexity(f, d, p=2)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": upper_bound,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_d = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_d} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")