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
    result = [[0.0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(p):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_norm(M):
    if not M:
        return 0.0
    return math.sqrt(sum(sum(x**2 for x in row) for row in M))

def power_iteration(M, max_iter=200, tol=1e-6):
    n = len(M)
    if n == 0:
        return 0.0, [0.0] * n
    b_k = [random.random() for _ in range(n)]
    b_k_norm = matrix_norm(b_k)
    if b_k_norm == 0:
        return 0.0, [0.0] * n
    b_k = [x / b_k_norm for x in b_k]

    for _ in range(max_iter):
        b_k1 = [sum(M[i][j] * b_k[j] for j in range(n)) for i in range(n)]
        b_k1_norm = matrix_norm(b_k1)
        if b_k1_norm == 0:
            return 0.0, [0.0] * n
        b_k1 = [x / b_k1_norm for x in b_k1]

        if abs(b_k1_norm - b_k_norm) < tol:
            break
        b_k = b_k1
        b_k_norm = b_k1_norm

    return b_k_norm, b_k

def compute_extreme_eigenvalues(M):
    if not M:
        return 0.0, 0.0
    lambda_max, _ = power_iteration(M)
    n = len(M)
    I = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    M_shifted = [[M[i][j] - lambda_max * I[i][j] for j in range(n)] for i in range(n)]
    lambda_min, _ = power_iteration(M_shifted)
    lambda_min += lambda_max
    return lambda_max, lambda_min

def generate_k_clique_dnf(v, k):
    edges = list(itertools.combinations(range(v), 2))
    terms = list(itertools.combinations(edges, k))
    return terms

def build_term_conflict_graph(terms):
    s = len(terms)
    adj_matrix = [[0.0 for _ in range(s)] for _ in range(s)]
    for i in range(s):
        for j in range(i + 1, s):
            if any(e in terms[j] for e in terms[i]):
                adj_matrix[i][j] = 1.0
                adj_matrix[j][i] = 1.0
    return adj_matrix

def compute_mu(terms, adj_matrix):
    s = len(terms)
    if s == 0:
        return 0.0
    lambda_max, lambda_min = compute_extreme_eigenvalues(adj_matrix)
    if lambda_max == 0:
        alpha_h = s
    else:
        alpha_h = -lambda_min * s / (lambda_max - lambda_min)
    max_term_size = max(len(term) for term in terms) if terms else 0
    if max_term_size == 0:
        return 0.0
    mu = s / (alpha_h * (1 + math.log2(1 + max_term_size)))
    return mu

def generate_random_dnf(n, s, k):
    terms = []
    for _ in range(s):
        term = random.sample(range(n), k)
        terms.append(term)
    return terms

def run_trial(seed):
    random.seed(seed)
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    # Test k-CLIQUE canonical DNF
    for v in range(5, 11):
        k = math.ceil(math.log2(v))
        terms = generate_k_clique_dnf(v, k)
        adj_matrix = build_term_conflict_graph(terms)
        mu = compute_mu(terms, adj_matrix)
        metric_values.append(mu / v)
        instances_tested += 1
        if mu < v / 16:
            conjecture_holds = False
            counterexample = f"k-CLIQUE canonical DNF with v={v}, mu={mu} < v/16"

    # Test random monotone DNFs
    for n in [15, 20, 25, 30, 40]:
        for s in [n, 2*n, 4*n, 8*n]:
            if s > 256:
                continue
            k = math.ceil(math.log2(n))
            terms = generate_random_dnf(n, s, k)
            adj_matrix = build_term_conflict_graph(terms)
            mu = compute_mu(terms, adj_matrix)
            metric_values.append(mu / math.log2(n))
            instances_tested += 1
            if mu > 8 * math.log2(n):
                conjecture_holds = False
                counterexample = f"Random monotone DNF with n={n}, s={s}, mu={mu} > 8*log2(n)"

    if not metric_values:
        return {
            "metric_name": "mu_ratio",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No instances tested"
        }

    avg_metric = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "mu_ratio",
        "metric_value": avg_metric,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = sys.argv[1:] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    trials = []
    for seed in seeds:
        trial = run_trial(seed)
        trials.append(trial)
        print(f"TRIAL: {trial}")

    metric_values = [trial["metric_value"] for trial in trials if trial["metric_value"] is not None]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_metric_values")
        sys.exit(0)

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for trial in trials if trial["conjecture_holds"]) / len(trials)

    if any(not trial["conjecture_holds"] for trial in trials):
        first_failing_seed = next(seed for seed, trial in zip(seeds, trials) if not trial["conjecture_holds"])
        counterexample = next(trial["counterexample"] for trial in trials if not trial["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")