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

def matrix_add(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matrix_scalar_multiply(A, scalar):
    return [[A[i][j] * scalar for j in range(len(A[0]))] for i in range(len(A))]

def matrix_subtract(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matrix_norm(A):
    return math.sqrt(sum(sum(x**2 for x in row) for row in A))

def power_iteration(A, num_iterations=200):
    n = len(A)
    b = [random.random() for _ in range(n)]
    for _ in range(num_iterations):
        b = matrix_multiply(A, [b])[0]
        norm = matrix_norm([b])
        if norm == 0:
            break
        b = [x / norm for x in b]
    return b

def deflation(A, b):
    n = len(A)
    outer = [[x * y for y in b] for x in b]
    return matrix_subtract(A, outer)

def compute_eigenvalues(A):
    n = len(A)
    if n == 0:
        return 0, 0
    A_copy = [row[:] for row in A]
    b_max = power_iteration(A_copy)
    lambda_max = sum(b_max[i] * sum(A_copy[i][j] * b_max[j] for j in range(n)) for i in range(n))
    A_deflated = deflation(A_copy, b_max)
    b_min = power_iteration(A_deflated)
    lambda_min = sum(b_min[i] * sum(A_deflated[i][j] * b_min[j] for j in range(n)) for i in range(n))
    return lambda_max, lambda_min

def compute_alpha_H(s, lambda_max, lambda_min):
    if lambda_max > 0:
        return -lambda_min * s / (lambda_max - lambda_min)
    else:
        return s

def compute_mu(s, alpha_H, max_term_size):
    if max_term_size <= 0:
        return 0
    return s / (alpha_H * (1 + math.log2(1 + max_term_size)))

def generate_random_dnf(n, s, k):
    terms = []
    for _ in range(s):
        term = set(random.sample(range(n), k))
        terms.append(term)
    return terms

def build_term_conflict_graph(terms):
    s = len(terms)
    adj = [[0 for _ in range(s)] for _ in range(s)]
    for i in range(s):
        for j in range(i + 1, s):
            if terms[i] & terms[j]:
                adj[i][j] = 1
                adj[j][i] = 1
    return adj

def generate_clique_dnf(v, k):
    n = v * (v - 1) // 2
    terms = []
    edges = list(itertools.combinations(range(v), 2))
    cliques = list(itertools.combinations(range(v), k))
    for clique in cliques:
        term = set()
        for edge in itertools.combinations(clique, 2):
            term.add(edges.index(edge))
        terms.append(term)
    return terms

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
        for s in [n, 2 * n, 4 * n, 8 * n]:
            if s > 256:
                continue
            terms = generate_random_dnf(n, s, k)
            adj = build_term_conflict_graph(terms)
            lambda_max, lambda_min = compute_eigenvalues(adj)
            alpha_H = compute_alpha_H(s, lambda_max, lambda_min)
            max_term_size = max(len(term) for term in terms) if terms else 0
            mu = compute_mu(s, alpha_H, max_term_size)
            metric_value = max(metric_value, mu / math.log2(n))
            instances_tested += 1
            if mu > 8 * math.log2(n):
                conjecture_holds = False
                counterexample = f"Random DNF with n={n}, s={s}, k={k}, mu={mu} > 8*log2(n)"

    # Test k-CLIQUE canonical DNFs
    for v in range(5, 11):
        k = math.ceil(math.log2(v))
        terms = generate_clique_dnf(v, k)
        adj = build_term_conflict_graph(terms)
        lambda_max, lambda_min = compute_eigenvalues(adj)
        alpha_H = compute_alpha_H(len(terms), lambda_max, lambda_min)
        max_term_size = max(len(term) for term in terms) if terms else 0
        mu = compute_mu(len(terms), alpha_H, max_term_size)
        metric_value = min(metric_value, mu / v) if metric_value != 0 else mu / v
        instances_tested += 1
        if mu < v / 16:
            conjecture_holds = False
            counterexample = f"k-CLIQUE DNF with v={v}, k={k}, mu={mu} < v/16"

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

    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0
    support_fraction = conjecture_holds_counts / len(seeds) if seeds else 0

    if counterexamples:
        print(f"RESULT: FALSIFIED counterexample={counterexamples[0]} first_failing_seed={seeds[counterexamples.index(counterexamples[0])]}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")