# auto-injected by SEC sandbox
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from fractions import Fraction

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

def matrix_transpose(A):
    return [list(row) for row in zip(*A)]

def matrix_subtract(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matrix_norm(A):
    return max(sum(abs(x) for x in row) for row in A)

def power_iteration(A, max_iter=200, tol=1e-6):
    n = len(A)
    b_k = [random.random() for _ in range(n)]
    for _ in range(max_iter):
        b_k1 = [sum(A[i][j] * b_k[j] for j in range(n)) for i in range(n)]
        b_k1_norm = math.sqrt(sum(x**2 for x in b_k1))
        b_k = [x / b_k1_norm for x in b_k1]
        if b_k1_norm < tol:
            break
    return b_k1_norm

def shifted_power_iteration(A, shift, max_iter=200, tol=1e-6):
    n = len(A)
    I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    A_shifted = matrix_subtract(A, [[shift * I[i][j] for j in range(n)] for i in range(n)])
    b_k = [random.random() for _ in range(n)]
    for _ in range(max_iter):
        b_k1 = [sum(A_shifted[i][j] * b_k[j] for j in range(n)) for i in range(n)]
        b_k1_norm = math.sqrt(sum(x**2 for x in b_k1))
        b_k = [x / b_k1_norm for x in b_k1]
        if b_k1_norm < tol:
            break
    return b_k1_norm

def compute_extreme_eigenvalues(A):
    lambda_max = power_iteration(A)
    lambda_min = -shifted_power_iteration(A, 0)
    return lambda_max, lambda_min

def compute_alpha_H(s, lambda_max, lambda_min):
    if lambda_max > 0:
        return -lambda_min * s / (lambda_max - lambda_min)
    else:
        return s

def compute_mu(F, s, alpha_H):
    max_term_size = max(len(term) for term in F) if F else 0
    if max_term_size == 0:
        return 0.0
    return s / (alpha_H * (1 + math.log2(1 + max_term_size)))

def generate_k_clique_dnf(v, k):
    edges = list(itertools.combinations(range(v), 2))
    terms = []
    for clique in itertools.combinations(range(v), k):
        term = []
        for i, j in itertools.combinations(clique, 2):
            term.append(edges.index((i, j)))
        terms.append(term)
    return terms

def generate_random_dnf(n, s, k):
    terms = []
    for _ in range(s):
        term = random.sample(range(n), k)
        terms.append(term)
    return terms

def build_term_conflict_graph(F):
    s = len(F)
    adj = [[0] * s for _ in range(s)]
    for i in range(s):
        for j in range(i + 1, s):
            if any(x in F[j] for x in F[i]):
                adj[i][j] = adj[j][i] = 1
    return adj

def run_trial(seed):
    random.seed(seed)
    metric_name = "mu"
    metric_value = 0.0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    # Test k-CLIQUE indicators
    for v in range(5, 11):
        k = math.ceil(math.log2(v))
        F = generate_k_clique_dnf(v, k)
        adj = build_term_conflict_graph(F)
        s = len(F)
        if s == 0:
            continue
        lambda_max, lambda_min = compute_extreme_eigenvalues(adj)
        alpha_H = compute_alpha_H(s, lambda_max, lambda_min)
        mu = compute_mu(F, s, alpha_H)
        instances_tested += 1
        if mu < v / 16:
            conjecture_holds = False
            counterexample = f"k-CLIQUE indicator for v={v} has mu={mu} < v/16"
            break

    if conjecture_holds:
        # Test random monotone DNFs
        for n in [15, 20, 25, 30, 40]:
            k = math.ceil(math.log2(n))
            for s in [n, 2 * n, 4 * n, 8 * n]:
                if s > 256:
                    continue
                F = generate_random_dnf(n, s, k)
                adj = build_term_conflict_graph(F)
                lambda_max, lambda_min = compute_extreme_eigenvalues(adj)
                alpha_H = compute_alpha_H(s, lambda_max, lambda_min)
                mu = compute_mu(F, s, alpha_H)
                instances_tested += 1
                if mu > 8 * math.log2(n):
                    conjecture_holds = False
                    counterexample = f"Random monotone DNF with n={n}, s={s}, k={k} has mu={mu} > 8*log2(n)"
                    break
            if not conjecture_holds:
                break

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
    counterexamples = []

    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        metric_values.append(trial["metric_value"])
        if trial["conjecture_holds"]:
            conjecture_holds_counts += 1
        if trial["counterexample"]:
            counterexamples.append(trial["counterexample"])

    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0.0
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0.0
    support_fraction = conjecture_holds_counts / len(seeds)

    if counterexamples:
        print(f"RESULT: FALSIFIED counterexample={counterexamples[0]} first_failing_seed={seeds[counterexamples.index(counterexamples[0])]}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")