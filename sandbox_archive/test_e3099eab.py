# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from itertools import combinations, chain

def binomial(n, k):
    if k > n:
        return 0
    result = 1
    for i in range(k):
        result *= (n - i)
        result //= (i + 1)
    return result

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    for j in range(n):
        pivot_row = None
        for i in range(rank, m):
            if A[i][j] != 0:
                pivot_row = i
                break
        if pivot_row is not None:
            A[pivot_row], A[rank] = A[rank], A[pivot_row]
            for i in range(m):
                if i != rank and A[i][j] != 0:
                    factor = A[i][j] / A[rank][j]
                    for k in range(n):
                        A[i][k] -= factor * A[rank][k]
            rank += 1
    return rank

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    m, n = len(A), len(A[0])
    if m != n:
        raise ValueError("Matrix must be square")
    if n == 1:
        return A[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        sign = (-1) ** j
        det += sign * A[0][j] * determinant(submatrix)
    return det

def powerset(s):
    result = []
    for r in range(len(s) + 1):
        result.extend(combinations(s, r))
    return result

def symmetric_function(n, R):
    def f(x):
        weight = sum(1 for bit in x if bit == '1')
        return weight in R
    return f

def dnf_min(f):
    n = len(next(iter(f.keys())))
    truth_table = ['0' * n + '1'] + [''.join(p) + '1' for p in powerset(range(n))]
    prime_implicants = []
    for minterm in truth_table:
        if f[minterm]:
            covered = False
            for pi in prime_implicants:
                if all(minterm[i] == '0' or minterm[i] == pi[i] for i in range(n)):
                    covered = True
                    break
            if not covered:
                prime_implicants.append(minterm)
    return len(prime_implicants)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [4, 5, 6, 7, 8, 10]
    metric_name = "DNF-min vs |χ(K_f)|"
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        R_samples = set()
        if n <= 7:
            R_samples.update(powerset(range(n + 1)))
        else:
            for _ in range(30):
                R = random.sample(range(n + 1), random.randint(1, n))
                R_samples.add(tuple(sorted(R)))

        for R in R_samples:
            f = symmetric_function(n, set(R))
            K_f = []
            for i in range(2**n):
                binary_rep = format(i, '0{}b'.format(n))
                if all(f[binary_rep[:j] + '1'] for j in range(len(binary_rep))):
                    K_f.append(binary_rep)

            chi_K_f = 0
            for d in range(n + 1):
                C_n_d = binomial(n, d)
                w_0s = [w for w in R if w >= d]
                chi_K_f += (-1)**d * C_n_d * sum(binomial(n - d, w_0) for w_0 in w_0s)

            dnf_min_f = dnf_min(f)
            instances_tested += 1

            if dnf_min_f < abs(chi_K_f):
                conjecture_holds = False
                counterexample = f"n={n}, R={R}"
                break

    return {
        "metric_name": metric_name,
        "metric_value": chi_K_f,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + list(range(53, 83))
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = (sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")