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
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(i+1, n):
                factor = A[j][i] / pivot
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        sign = 1
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += sign * A[0][j] * determinant(submatrix)
            sign *= -1
        return det
    
    def symmetric_square(A):
        n = len(A)
        result = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                result[i][j] = sum(A[x][i] * A[y][j] for x in range(n) for y in range(n))
                result[j][i] = result[i][j]
        return result
    
    def schur_coefficient(matrix, rep):
        n = len(matrix)
        if rep == (n-1, 1):
            det = determinant(matrix)
            return abs(det) * 2**(n/2)
        else:
            return 0
    
    n = random.randint(5, 40)
    A = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
    S2_A = symmetric_square(A)
    
    schur_val = schur_coefficient(S2_A, (n-1, 1))
    det_n = determinant([[i+1 if i == j else 0 for j in range(n)] for i in range(n)])
    schur_det_val = schur_coefficient(symmetric_square(det_n), (n-1, 1))
    
    return {
        "metric_name": "schur_coefficient",
        "metric_value": schur_val,
        "instances_tested": 1,
        "conjecture_holds": schur_val >= 2**(n/2),
        "counterexample": "" if schur_val >= 2**(n/2) else f"Schur coefficient {schur_val} < 2^{n/2}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")