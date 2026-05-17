# auto-injected by SEC sandbox
import itertools
import collections
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import json
from fractions import Fraction

def matrix_multiply(A, B):
    """Multiply two matrices A and B."""
    if not A or not B or len(A[0]) != len(B):
        raise ValueError("Incompatible matrix dimensions for multiplication")
    result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_subtract(A, B):
    """Subtract matrix B from matrix A."""
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        raise ValueError("Matrices must have the same dimensions for subtraction")
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matrix_transpose(A):
    """Transpose a matrix A."""
    return [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]

def matrix_norm_frobenius(A):
    """Compute the Frobenius norm of matrix A."""
    return math.sqrt(sum(sum(a ** 2 for a in row) for row in A))

def matrix_norm_op(A):
    """Compute the operator norm (spectral norm) of matrix A."""
    # Using the power iteration method to approximate the largest singular value
    if not A or not A[0]:
        return 0.0
    b_k = [random.random() for _ in range(len(A[0]))]
    for _ in range(100):
        # Multiply A and b_k
        b_k = [sum(A[i][j] * b_k[j] for j in range(len(b_k))) for i in range(len(A))]
        # Normalize b_k
        norm = math.sqrt(sum(x ** 2 for x in b_k))
        if norm == 0:
            break
        b_k = [x / norm for x in b_k]
    # Compute A*b_k
    Ab_k = [sum(A[i][j] * b_k[j] for j in range(len(b_k))) for i in range(len(A))]
    # Compute the norm of A*b_k
    norm_Ab_k = math.sqrt(sum(x ** 2 for x in Ab_k))
    return norm_Ab_k

def compute_stable_rank(S):
    """Compute the stable rank of matrix S."""
    if not S or not S[0]:
        return 0.0
    frobenius_norm = matrix_norm_frobenius(S)
    op_norm = matrix_norm_op(S)
    if op_norm == 0:
        return 0.0
    return frobenius_norm ** 2 / op_norm ** 2

def generate_random_bp(n, w, seed):
    """Generate a random read-twice BP of size w and n variables."""
    random.seed(seed)
    s = w
    layers = 4 * n
    M = []
    for _ in range(layers):
        M_t_0 = [[random.randint(0, 1) for _ in range(s)] for _ in range(s)]
        M_t_1 = [[random.randint(0, 1) for _ in range(s)] for _ in range(s)]
        M.append((M_t_0, M_t_1))
    return M, s

def construct_symbol_matrix(M, s):
    """Construct the symbol matrix S(P) from the transition matrices M."""
    layers = len(M)
    S = []
    for M_t_0, M_t_1 in M:
        Delta_t = matrix_subtract(M_t_1, M_t_0)
        S.extend(Delta_t)
    # Reshape S into an s x (4n * s) matrix
    reshaped_S = []
    for i in range(s):
        row = []
        for j in range(0, len(S), s):
            row.extend(S[j + i])
        reshaped_S.append(row)
    return reshaped_S

def evaluate_bp(M, s, n):
    """Evaluate the BP on all 2^{2n} inputs."""
    inputs = []
    for i in range(2 ** (2 * n)):
        inputs.append([(i >> j) & 1 for j in range(2 * n)])
    outputs = []
    for input_bits in inputs:
        state = [1 if i == 0 else 0 for i in range(s)]
        for t in range(4 * n):
            M_t_0, M_t_1 = M[t]
            b = input_bits[t % (2 * n)]
            if b == 0:
                M_t = M_t_0
            else:
                M_t = M_t_1
            new_state = [0] * s
            for i in range(s):
                for j in range(s):
                    new_state[i] += state[j] * M_t[j][i]
            state = new_state
        outputs.append(state[0])
    return outputs

def compute_correlation(outputs, n):
    """Compute the correlation of the BP outputs with IP_2."""
    ip2_outputs = []
    for i in range(2 ** (2 * n)):
        x = [(i >> j) & 1 for j in range(n)]
        y = [(i >> (n + j)) & 1 for j in range(n)]
        ip2_outputs.append(1 if sum(x[j] & y[j] for j in range(n)) % 2 == 0 else -1)
    correlation = sum(outputs[i] * ip2_outputs[i] for i in range(len(outputs))) / len(outputs)
    return correlation

def run_trial(seed):
    """Run a single trial with the given seed."""
    random.seed(seed)
    n_values = [3, 4, 5, 6]
    w_values = [4, 8, 16]
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    metric_values = []

    for n in n_values:
        for w in w_values:
            M, s = generate_random_bp(n, w, seed)
            S = construct_symbol_matrix(M, s)
            rho = compute_stable_rank(S)
            outputs = evaluate_bp(M, s, n)
            epsilon = compute_correlation(outputs, n)
            metric_values.append(rho)

            if rho > 2 * s:
                conjecture_holds = False
                counterexample = f"BP with rho={rho} > 2s={2*s}"
                break
            if epsilon >= 0.25 and rho < 0.05 * epsilon ** 2 * (2 ** (n / 2)):
                conjecture_holds = False
                counterexample = f"BP with epsilon={epsilon} >= 0.25 and rho={rho} < 0.05 * epsilon^2 * 2^(n/2)"
                break
            instances_tested += 1

        if not conjecture_holds:
            break

    if conjecture_holds:
        # Test the canonical IP_2 BP
        n = 3  # Smallest n for IP_2
        s = 2 ** n
        M = []
        for t in range(4 * n):
            M_t_0 = [[0 for _ in range(s)] for _ in range(s)]
            M_t_1 = [[0 for _ in range(s)] for _ in range(s)]
            for i in range(s):
                for j in range(s):
                    if t < 2 * n:
                        if (i >> t) & 1 == (j >> t) & 1:
                            M_t_0[i][j] = 1
                            M_t_1[i][j] = 1
                    else:
                        if (i >> (t - 2 * n)) & 1 == (j >> (t - 2 * n)) & 1:
                            M_t_0[i][j] = 1
                            M_t_1[i][j] = 1
            M.append((M_t_0, M_t_1))
        S = construct_symbol_matrix(M, s)
        rho = compute_stable_rank(S)
        outputs = evaluate_bp(M, s, n)
        epsilon = compute_correlation(outputs, n)
        metric_values.append(rho)

        if rho > 2 * s:
            conjecture_holds = False
            counterexample = f"IP_2 BP with rho={rho} > 2s={2*s}"
        if epsilon >= 0.25 and rho < 0.05 * epsilon ** 2 * (2 ** (n / 2)):
            conjecture_holds = False
            counterexample = f"IP_2 BP with epsilon={epsilon} >= 0.25 and rho={rho} < 0.05 * epsilon^2 * 2^(n/2)"
        instances_tested += 1

    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0.0
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0.0

    return {
        "metric_name": "stable_rank",
        "metric_value": mean_metric,
        "metric_std": std_metric,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = sys.argv[1:] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        result["seed"] = seed
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)

    mean_metric = sum(r["metric_value"] for r in results) / len(results)
    std_metric = math.sqrt(sum((r["metric_value"] - mean_metric) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={r['seed']}")
                break