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
            max_row = max(range(i, n), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
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

    def svd(A):
        U, S, Vt = [], [], []
        n = len(A)
        Q, R = gaussian_elimination(A), [[A[j][i] for j in range(n)] for i in range(n)]
        for i in range(n):
            u_i = [R[i][j] / math.sqrt(sum(R[j][k]**2 for k in range(n))) for j in range(n)]
            U.append(u_i)
            s_i = sum(u_i[k] * R[k][i] for k in range(n))
            S.append(s_i)
            v_i = [R[j][i] / s_i if abs(s_i) > 1e-9 else 0 for j in range(n)]
            Vt.append(v_i)
        return U, S, Vt

    def det(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det_val = 0
        sign = 1
        for i in range(n):
            submatrix = [row[:i] + row[i+1:] for row in A[1:]]
            det_val += sign * A[0][i] * det(submatrix)
            sign *= -1
        return det_val

    def random_subsets(rows, cols, r):
        rows_set = set(random.sample(range(len(rows)), r))
        cols_set = set(random.sample(range(len(cols)), r))
        submatrix = [[rows[i][j] for j in cols_set] for i in rows_set]
        return submatrix

    def max_det_power(A, r):
        n = len(A)
        max_det = 0
        for _ in range(2000):
            submatrix = random_subsets(A, A[0], r)
            det_val = abs(det(submatrix))
            if det_val > max_det:
                max_det = det_val
        return max_det**(2/r)

    def frobenius_norm(A):
        n = len(A)
        norm = 0
        for i in range(n):
            for j in range(n):
                norm += A[i][j]**2
        return math.sqrt(norm)

    def run_trial_inner(N, r):
        M = [[random.choice([-1, 1]) for _ in range(N)] for _ in range(N)]
        U, S, Vt = svd(M)
        sigma_r = S[r-1]
        D_r = max_det_power(M, r)
        return {"sigma_r": sigma_r, "D_r": D_r}

    n_values = [8, 16, 32]
    r_values = [2, 3, 4]
    results = []
    
    for N in n_values:
        for r in r_values:
            result = run_trial_inner(N, r)
            sigma_r = result["sigma_r"]
            D_r = result["D_r"]
            ratio = 4 * sigma_r**2 / D_r
            results.append({"N": N, "r": r, "ratio": ratio})
    
    min_ratio = min(result["ratio"] for result in results)
    mean_ratio = sum(result["ratio"] for result in results) / len(results)
    
    return {
        "metric_name": "4 * sigma_r^2 / D_r",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "conjecture_holds": min_ratio >= 1.0 and mean_ratio >= 1.5,
        "counterexample": "" if min_ratio >= 1.0 else f"min_ratio={min_ratio}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(3, 6)]
    
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")