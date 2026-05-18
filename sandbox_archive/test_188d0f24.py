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
            A[i] = [x * factor for x in A[i]]
            for j in range(n):
                if i != j:
                    factor = A[j][i]
                    A[j] = [A[j][k] - factor * A[i][k] for k in range(n)]
        return A

    def matrix_multiplication(A, B):
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
        for i in range(len(A)):
            submatrix = [row[:i] + row[i+1:] for row in A[1:]]
            det += sign * A[0][i] * determinant(submatrix)
            sign *= -1
        return det

    def svd(A):
        U, S, Vt = [], [], []
        n, m = len(A), len(A[0])
        if n > m:
            A = list(zip(*A))
            n, m = m, n
        
        Q, R = [], []
        for i in range(n):
            Q.append([random.gauss(0, 1) for _ in range(m)])
        
        while True:
            Q = gaussian_elimination(Q)
            R = [[sum(Q[i][j] * A[j][k] for j in range(m)) for k in range(m)] for i in range(n)]
            
            QR = matrix_multiplication(Q, R)
            QRtQR = matrix_multiplication(QR, QR)
            U = gaussian_elimination(QRtQR)
            
            UTU = [[sum(U[i][j] * U[k][j] for j in range(m)) for k in range(n)] for i in range(n)]
            S = [math.sqrt(UTU[i][i]) if UTU[i][i] != 0 else 0 for i in range(n)]
            
            Vt = [[sum(Q[j][k] * R[k][i] / S[i] for k in range(m)) if S[i] != 0 else 0 for j in range(n)] for i in range(m)]
            break
        
        return U, S, Vt

    def generate_random_sign_matrix(N):
        return [[random.choice([-1, 1]) for _ in range(N)] for _ in range(N)]

    def generate_sylvester_hadamard_matrix(N):
        if N == 1:
            return [[1]]
        H = generate_sylvester_hadamard_matrix(N // 2)
        a = [1] * (N // 2) + [-1] * (N // 2)
        b = [1] * (N // 2) + [1] * (N // 2)
        return [[a[i] * H[j][k] for k in range(N // 2)] + [b[i] * H[j][k] for k in range(N // 2)]
                for i in range(N // 2)] + [[b[i] * H[j][k] for k in range(N // 2)] + [a[i] * H[j][k] for k in range(N // 2)]
                                          for i in range(N // 2)]

    def generate_padded_identity_matrix(N, k):
        I = [[1 if i == j else 0 for j in range(k)] for i in range(k)]
        return [[I[i % k][j % k] if i < N and j < N else 0 for j in range(N)] for i in range(N)]

    def generate_low_rank_plus_noise_matrix(N, k):
        A = generate_random_sign_matrix(N)
        U, _, Vt = svd(A)
        U = [[U[i][j] * random.gauss(1, 0.1) for j in range(k)] for i in range(N)]
        Vt = [[Vt[j][i] * random.gauss(1, 0.1) for j in range(k)] for i in range(k)]
        return matrix_multiplication(matrix_multiplication(U, [[random.choice([-1, 1]) for _ in range(k)] for _ in range(k)]), Vt)

    def generate_cyclic_shift_matrix(N):
        row = [1 if i % N == j else 0 for j in range(N)]
        return [row[i:] + row[:i] for i in range(N)]

    ensembles = [
        generate_random_sign_matrix,
        generate_sylvester_hadamard_matrix,
        generate_padded_identity_matrix,
        lambda N: generate_low_rank_plus_noise_matrix(N, min(5, N // 2)),
        generate_cyclic_shift_matrix
    ]

    n_values = [8, 16, 32]
    r_values = [2, 3, 4]
    num_trials = 2000

    min_ratio = float('inf')
    counterexample = ""

    for N in n_values:
        for _ in range(5):
            M = ensembles[random.randint(0, len(ensembles) - 1)](N)
            U, S, Vt = svd(M)
            
            for r in r_values:
                max_det = 0
                for _ in range(num_trials):
                    rows = random.sample(range(N), r)
                    cols = random.sample(range(N), r)
                    A = [[M[i][j] for j in cols] for i in rows]
                    det = abs(determinant(A))
                    if det > max_det:
                        max_det = det
                
                D_r = max_det ** (2 / r)
                sigma_r_squared = S[r-1] ** 2
                ratio = 4 * sigma_r_squared / D_r
                if ratio < min_ratio:
                    min_ratio = ratio
                    counterexample = f"({N}, {r})"

    return {
        "metric_name": "min_ratio",
        "metric_value": min_ratio,
        "instances_tested": num_trials * len(n_values) * 5 * len(r_values),
        "conjecture_holds": min_ratio >= 1.0,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + random.randint(0, 31) for i in range(3, 6)]
    
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)

    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")