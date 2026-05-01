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

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def gaussian_elimination(A, b=None):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda x: abs(A[x][i]))
        A[i], A[max_row] = A[max_row], A[i]
        if b is not None:
            b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            if b is not None:
                b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def matrix_multiply(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def eigenvalue_decomposition(A):
    n = len(A)
    if n != len(A[0]):
        raise ValueError("Matrix must be square")
    tolerance = 1e-6
    max_iterations = 1000
    v = [random.random() for _ in range(n)]
    for iteration in range(max_iterations):
        w = matrix_multiply(A, v)
        lambda_ = sum(w[i] * v[i] for i in range(n)) / sum(v[i]**2 for i in range(n))
        v_next = [w[i] - lambda_ * v[i] for i in range(n)]
        norm = math.sqrt(sum(v_next[i]**2 for i in range(n)))
        v_next = [v_next[i] / norm for i in range(n)]
        if sum((v_next[i] - v[i])**2 for i in range(n)) < tolerance:
            return lambda_, v_next
        v = v_next
    raise ValueError("Failed to converge")

def degree_d_sos_moment_matrix(G, d):
    n = len(G)
    M = [[0] * (n**d) for _ in range(n**d)]
    for i in range(n):
        for j in range(i + 1, n):
            if G[i][j]:
                for k in range(d):
                    M[i*n**(k-1):(i+1)*n**(k-1), j*n**(k-1):(j+1)*n**(k-1)] += [[G[i][j]] * n**(2*k-2)]
    return M

def max_cut_instance(n, density=0.5):
    G = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < density:
                G[i][j] = G[j][i] = 1
    return G

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    d_values = [2, 3, 4]
    support_count = 0
    total_rank = 0
    instances_tested = 0
    counterexample = ""

    for n in n_values:
        for _ in range(5):
            G = max_cut_instance(n)
            for d in d_values:
                M = degree_d_sos_moment_matrix(G, d)
                _, v = eigenvalue_decomposition(M)
                rank = sum(1 for x in v if abs(x) > 1e-6)
                instances_tested += 1
                total_rank += rank
                if rank < n**(1 - 1/d):
                    support_count += 1
                    counterexample = f"n={n}, d={d}, rank={rank}"
                    break

    mean_rank = total_rank / instances_tested
    support_fraction = support_count / instances_tested * 100
    conjecture_holds = support_fraction >= 80

    return {
        "metric_name": "Mean Rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or generate_primes(30)
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    mean_rank = total_rank / instances_tested
    support_fraction = support_count / instances_tested * 100

    if conjecture_holds:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_deviation:.2f} support_fraction={support_fraction:.2f}")
    elif counterexample:
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[0]}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")