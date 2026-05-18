# auto-injected by SEC sandbox
import json
import os
import time
import re
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from collections import defaultdict

def matrix_multiply(A, B):
    n = len(A)
    m = len(B[0])
    p = len(B)
    result = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(p):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_transpose(M):
    return [list(row) for row in zip(*M)]

def matrix_add(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matrix_subtract(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matrix_scalar_multiply(M, scalar):
    return [[M[i][j] * scalar for j in range(len(M[0]))] for i in range(len(M))]

def matrix_norm(M):
    return math.sqrt(sum(sum(x**2 for x in row) for row in M))

def power_iteration(M, max_iter=200, tol=1e-6):
    n = len(M)
    b_k = [random.random() for _ in range(n)]
    b_k_norm = matrix_norm(b_k)
    b_k = [x / b_k_norm for x in b_k]

    for _ in range(max_iter):
        b_k1 = [sum(M[i][j] * b_k[j] for j in range(n)) for i in range(n)]
        b_k1_norm = matrix_norm(b_k1)
        b_k1 = [x / b_k1_norm for x in b_k1]

        if abs(b_k1_norm - b_k_norm) < tol:
            break
        b_k = b_k1
        b_k_norm = b_k1_norm

    return b_k_norm

def shifted_power_iteration(M, shift, max_iter=200, tol=1e-6):
    n = len(M)
    I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    M_shifted = matrix_subtract(M, matrix_scalar_multiply(I, shift))
    return power_iteration(M_shifted, max_iter, tol) + shift

def compute_extreme_eigenvalues(adj_matrix):
    n = len(adj_matrix)
    if n == 0:
        return 0, 0

    lambda_max = power_iteration(adj_matrix)
    lambda_min = -shifted_power_iteration(adj_matrix, 0)

    return lambda_max, lambda_min

def compute_alpha_H(s, lambda_max, lambda_min):
    if lambda_max > 0:
        return -lambda_min * s / (lambda_max - lambda_min)
    else:
        return s

def compute_mu(s, alpha_H, max_term_size):
    if alpha_H == 0:
        return float('inf')
    log_term = math.log2(1 + max_term_size)
    if log_term <= 0:
        return float('inf')
    return s / (alpha_H * (1 + log_term))

def generate_random_dnf(n, s, k):
    terms = []
    for _ in range(s):
        term = random.sample(range(n), k)
        terms.append(set(term))
    return terms

def generate_clique_dnf(v, k):
    edges = list(itertools.combinations(range(v), 2))
    terms = []
    for clique in itertools.combinations(range(v), k):
        term = []
        for i, j in itertools.combinations(clique, 2):
            term.append(edges.index((i, j)))
        terms.append(set(term))
    return terms

def build_term_conflict_graph(terms):
    s = len(terms)
    adj_matrix = [[0 for _ in range(s)] for _ in range(s)]
    for i in range(s):
        for j in range(i + 1, s):
            if terms[i] & terms[j]:
                adj_matrix[i][j] = 1
                adj_matrix[j][i] = 1
    return adj_matrix

def run_trial(seed):
    random.seed(seed)
    metric_name = "mu"
    metric_value = 0.0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    # Test random monotone DNFs
    for n in [15, 20, 25, 30, 40]:
        k = math.ceil(math.log2(n))
        for s in [n, 2*n, 4*n, 8*n]:
            if s > 256:
                continue
            terms = generate_random_dnf(n, s, k)
            adj_matrix = build_term_conflict_graph(terms)
            lambda_max, lambda_min = compute_extreme_eigenvalues(adj_matrix)
            alpha_H = compute_alpha_H(s, lambda_max, lambda_min)
            max_term_size = max(len(term) for term in terms)
            mu = compute_mu(s, alpha_H, max_term_size)
            metric_value = max(metric_value, mu / math.log2(n))
            instances_tested += 1
            if mu > 8 * math.log2(n):
                conjecture_holds = False
                counterexample = f"Random DNF with n={n}, s={s}, k={k} has mu={mu} > 8*log2(n)"

    # Test k-CLIQUE canonical DNFs
    for v in range(5, 11):
        k = math.ceil(math.log2(v))
        terms = generate_clique_dnf(v, k)
        adj_matrix = build_term_conflict_graph(terms)
        lambda_max, lambda_min = compute_extreme_eigenvalues(adj_matrix)
        alpha_H = compute_alpha_H(len(terms), lambda_max, lambda_min)
        max_term_size = max(len(term) for term in terms)
        mu = compute_mu(len(terms), alpha_H, max_term_size)
        metric_value = min(metric_value, mu / v) if metric_value != 0 else mu / v
        instances_tested += 1
        if mu < v / 16:
            conjecture_holds = False
            counterexample = f"k-CLIQUE canonical DNF with v={v}, k={k} has mu={mu} < v/16"

    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]

    metric_values = []
    conjecture_holds_counts = 0

    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        metric_values.append(trial["metric_value"])
        if trial["conjecture_holds"]:
            conjecture_holds_counts += 1

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = conjecture_holds_counts / len(seeds)

    if all(trial["conjecture_holds"] for trial in [run_trial(seed) for seed in seeds]):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        for seed in seeds:
            trial = run_trial(seed)
            if not trial["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{trial['counterexample']}\" first_failing_seed={seed}")
                break