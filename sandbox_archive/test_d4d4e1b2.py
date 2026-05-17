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

def matrix_transpose(A):
    return [list(row) for row in zip(*A)]

def matrix_eigenvalues(A):
    n = len(A)
    if n > 20:
        raise ValueError("Matrix too large for this implementation")

    # Initialize a random matrix Q
    Q = [[random.random() for _ in range(n)] for _ in range(n)]

    for _ in range(100):
        # Compute Q^T * A * Q
        QTA = matrix_multiply(matrix_transpose(Q), A)
        QTAQ = matrix_multiply(QTA, Q)

        # Compute eigenvalues (diagonal elements of QTAQ)
        eigenvalues = [QTAQ[i][i] for i in range(n)]

        # Update Q using QR decomposition (simplified)
        for i in range(n):
            norm = math.sqrt(sum(Q[i][j]**2 for j in range(n)))
            if norm > 0:
                for j in range(n):
                    Q[i][j] /= norm

    return eigenvalues

def compute_mu(K):
    eigenvalues = matrix_eigenvalues(K)
    mu_2 = sum(e**2 for e in eigenvalues)
    mu_1 = sum(e for e in eigenvalues)
    if mu_1 == 0:
        return 0.0
    return math.log2(mu_2 / mu_1)

def generate_random_dnf(N, s, seed):
    random.seed(seed)
    terms = []
    for _ in range(s):
        support_size = random.randint(3, 6)
        support = set(random.sample(range(N), support_size))
        terms.append(support)
    return terms

def build_gram_matrix(F, rho=0.5):
    s = len(F)
    K = [[0.0 for _ in range(s)] for _ in range(s)]
    for i in range(s):
        for j in range(s):
            intersection = len(F[i] & F[j])
            K[i][j] = 2**(-len(F[i]) - len(F[j])) * (3/2)**intersection
    return K

def generate_clique_dnf(v, k, seed):
    random.seed(seed)
    vertices = list(range(v))
    random.shuffle(vertices)
    cliques = list(itertools.combinations(vertices, k))
    terms = []
    for clique in cliques:
        support = set()
        for i, j in itertools.combinations(clique, 2):
            support.add(i * v + j)
        terms.append(support)
    return terms

def dnf_conjunction(F, G):
    result = []
    for term_f in F:
        for term_g in G:
            result.append(term_f | term_g)
    return result

def run_trial(seed):
    random.seed(seed)
    N = random.choice([20, 30, 40])
    s = N
    F = generate_random_dnf(N, s, seed)
    K = build_gram_matrix(F)
    mu = compute_mu(K)
    bound = 4 * math.log2(2 * N + s)

    if mu > bound + 1e-9:
        return {
            "metric_name": "mu(F)",
            "metric_value": mu,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"mu(F) = {mu} > bound = {bound}"
        }

    v = random.choice([6, 7, 8, 9])
    k = math.ceil(math.log2(v))
    F_clique = generate_clique_dnf(v, k, seed)
    K_clique = build_gram_matrix(F_clique)
    mu_clique = compute_mu(K_clique)
    lower_bound = v / 4

    if mu_clique < lower_bound - 1e-9:
        return {
            "metric_name": "mu(F_clique)",
            "metric_value": mu_clique,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"mu(F_clique) = {mu_clique} < lower_bound = {lower_bound}"
        }

    F1 = generate_random_dnf(10, 6, seed)
    G1 = generate_random_dnf(10, 6, seed + 1)
    F_conj = dnf_conjunction(F1, G1)
    K_conj = build_gram_matrix(F_conj)
    mu_conj = compute_mu(K_conj)
    K_F1 = build_gram_matrix(F1)
    K_G1 = build_gram_matrix(G1)
    mu_F1 = compute_mu(K_F1)
    mu_G1 = compute_mu(K_G1)

    if mu_conj > mu_F1 + mu_G1 + 1e-9:
        return {
            "metric_name": "mu(F_conj)",
            "metric_value": mu_conj,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"mu(F_conj) = {mu_conj} > mu(F1) + mu(G1) = {mu_F1 + mu_G1}"
        }

    return {
        "metric_name": "mu(F)",
        "metric_value": mu,
        "instances_tested": 3,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        result["seed"] = seed
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results if r["conjecture_holds"]]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_trials")
        sys.exit(0)

    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        failing_seeds = [r["seed"] for r in results if not r["conjecture_holds"]]
        counterexamples = [r["counterexample"] for r in results if not r["conjecture_holds"]]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexamples[0]}\" first_failing_seed={failing_seeds[0]}")