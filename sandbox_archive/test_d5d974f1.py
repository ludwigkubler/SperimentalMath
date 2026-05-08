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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = max(range(i, n), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def solve_linear_system(A, b):
    n = len(A)
    A_b = [A[i] + [b[i]] for i in range(n)]
    gaussian_elimination(A_b)
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (A_b[i][-1] - sum(A_b[i][j] * x[j] for j in range(i + 1, n))) / A_b[i][i]
    return x

def matrix_multiply(A, B):
    m, k = len(A), len(B[0])
    result = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(len(B)):
                result[i][j] += A[i][l] * B[l][j]
    return result

def svd(A):
    m, n = len(A), len(A[0])
    U = [[A[i][j] for j in range(n)] for i in range(m)]
    Vt = [[0] * m for _ in range(n)]
    S = [0] * min(m, n)
    
    # Compute A^T * A and A * A^T
    AtA = matrix_multiply(A, A)
    AA = matrix_multiply(A, A)
    
    # Perform QR decomposition on A^T * A and A * A^T
    Q1, R1 = qr_decomposition(AtA)
    Q2, R2 = qr_decomposition(AA)
    
    # Compute U, S, Vt
    U = matrix_multiply(Q1, Q2)
    for i in range(min(m, n)):
        S[i] = math.sqrt(R1[i][i] * R2[i][i])
        Vt[i] = [R2[i][j] / S[i] if j == i else 0 for j in range(n)]
    
    return U, S, Vt

def qr_decomposition(A):
    m, n = len(A), len(A[0])
    Q = [[A[i][j] for j in range(n)] for i in range(m)]
    R = [[0 if j < i else A[i][j] for j in range(n)] for i in range(m)]
    
    for k in range(n):
        norm_qk = sum(Q[i][k]**2 for i in range(k, m))**0.5
        Q[k][k] /= norm_qk
        R[k][k] = norm_qk
        
        for j in range(k + 1, n):
            R[k][j] = sum(Q[i][k] * Q[i][j] for i in range(k, m))
            for i in range(m):
                Q[i][j] -= Q[i][k] * R[k][j]
    
    return Q, R

def log_energy_deficit(M_f):
    U, S, Vt = svd(M_f)
    N = len(S)
    sigma_i_over_sqrt_N = [sigma / math.sqrt(N) for sigma in S]
    delta_E = 0.5 * math.log(sigma_i_over_sqrt_N[0]**2 / N)
    for i in range(1, N):
        for j in range(i + 1, N):
            delta_E -= (2 / (N * (N - 1))) * math.log(abs(sigma_i_over_sqrt_N[i] / math.sqrt(N) - sigma_i_over_sqrt_N[j] / math.sqrt(N)))
    return delta_E

def sign_communication_matrix(f):
    n = len(f)
    M_f = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            M_f[i][j] = 1 if f(i) == f(j) else -1
    return M_f

def generate_disjunctive_function(n):
    def f(x):
        return all(x[i] == x[0] for i in range(1, n))
    return f

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    
    for n in [2, 3, 4, 5, 6, 7, 8]:
        for _ in range(30):
            if n == 2:
                f = generate_disjunctive_function(n)
            elif n == 3:
                # Implement IP_n here
                pass
            elif n == 4:
                # Implement EQ_n here
                pass
            elif n == 5:
                # Implement GT_n here
                pass
            elif n == 6:
                # Implement INDEX_n here
                pass
            elif n == 7:
                # Implement MAJ-of-AND here
                pass
            else:
                f = lambda x: random.choice([-1, 1])
            
            M_f = sign_communication_matrix(f)
            delta_E = log_energy_deficit(M_f)
            disc_bound = 1 / (2 ** n * math.sqrt(n))
            disc_sampled = 0.5
            disc = min(disc_bound, disc_sampled)
            results.append((n, delta_E, disc))
    
    if not results:
        return {
            "metric_name": "log₂(1/disc)",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    log2_disc = [math.log2(1 / disc) for _, _, disc in results]
    n_delta_E_over_16 = [(n * delta_E / 16) for n, delta_E, _ in results]
    mean_log2_disc = sum(log2_disc) / len(log2_disc)
    mean_n_delta_E_over_16 = sum(n_delta_E_over_16) / len(n_delta_E_over_16)
    
    slope, intercept = 0, 0
    for n, delta_E in zip(range(2, 9), [mean_n_delta_E_over_16] * 7):
        slope += (n - mean_n_delta_E_over_16) * (math.log2(1 / disc_bound) - n * delta_E / 16)
    slope /= sum((n - mean_n_delta_E_over_16)**2 for n in range(2, 9))
    
    r_squared = sum((log2_disc[i] - intercept - slope * n_delta_E_over_16[i])**2 for i in range(len(log2_disc))) / len(log2_disc)
    
    conjecture_holds = all(n * delta_E / 16 <= math.log2(1 / disc) + 3 for _, delta_E, disc in results)
    conjecture_holds &= slope >= 1.0 and r_squared >= 0.7
    conjecture_holds &= mean_n_delta_E_over_16[5] >= 0.12 and mean_n_delta_E_over_16[6] >= 0.12 and mean_n_delta_E_over_16[7] >= 0.12
    
    return {
        "metric_name": "log₂(1/disc)",
        "metric_value": mean_log2_disc,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(2, 6)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")