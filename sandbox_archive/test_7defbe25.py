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

def matrix_eigenvalues(A):
    n = len(A)
    if n > 20:
        raise ValueError("Matrix too large for this implementation")
    eigenvalues = []
    for _ in range(100):
        x = [random.random() for _ in range(n)]
        for _ in range(100):
            y = [0.0 for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    y[i] += A[i][j] * x[j]
            norm = math.sqrt(sum(yi**2 for yi in y))
            if norm == 0:
                break
            x = [yi / norm for yi in y]
        eigenvalue = sum(x[i] * sum(A[i][j] * x[j] for j in range(n)) for i in range(n))
        eigenvalues.append(eigenvalue)
    return sorted(eigenvalues)

def compute_mu(K):
    eigenvalues = matrix_eigenvalues(K)
    sum_lambda = sum(eigenvalues)
    sum_lambda_squared = sum(eigenvalue**2 for eigenvalue in eigenvalues)
    if sum_lambda_squared == 0:
        return 0.0
    mu = math.log2((sum_lambda_squared) / (sum_lambda**2))
    return mu

def generate_random_dnf(N, s, seed):
    random.seed(seed)
    terms = []
    for _ in range(s):
        support_size = random.randint(3, 6)
        support = random.sample(range(N), support_size)
        terms.append(set(support))
    return terms

def build_gram_matrix(F, rho=0.5):
    s = len(F)
    K = [[0.0 for _ in range(s)] for _ in range(s)]
    for i in range(s):
        for j in range(s):
            intersection_size = len(F[i] & F[j])
            K[i][j] = 2**(-len(F[i]) - len(F[j])) * (1.5)**intersection_size
    return K

def generate_k_clique_dnf(v, k, seed):
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
    conjecture_holds = mu <= bound + 1e-9

    if not conjecture_holds:
        return {
            "metric_name": "mu_upper_bound",
            "metric_value": mu,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"mu={mu} > bound={bound} for N={N}, s={s}"
        }

    v = random.choice([6, 7, 8, 9])
    k = math.ceil(math.log2(v))
    F_clique = generate_k_clique_dnf(v, k, seed)
    K_clique = build_gram_matrix(F_clique)
    mu_clique = compute_mu(K_clique)
    lower_bound = v / 4
    conjecture_holds_clique = mu_clique >= lower_bound - 1e-9

    if not conjecture_holds_clique:
        return {
            "metric_name": "mu_lower_bound",
            "metric_value": mu_clique,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"mu={mu_clique} < bound={lower_bound} for v={v}, k={k}"
        }

    N_submod = 20
    s_submod = random.choice([6, 8])
    F_submod = generate_random_dnf(N_submod, s_submod, seed)
    G_submod = generate_random_dnf(N_submod, s_submod, seed + 1)
    F_conj = dnf_conjunction(F_submod, G_submod)
    K_submod = build_gram_matrix(F_submod)
    K_conj = build_gram_matrix(F_conj)
    mu_submod = compute_mu(K_submod)
    mu_conj = compute_mu(K_conj)
    conjecture_holds_submod = mu_conj <= mu_submod + 1e-9

    if not conjecture_holds_submod:
        return {
            "metric_name": "mu_submodularity",
            "metric_value": mu_conj,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"mu_conj={mu_conj} > mu_submod={mu_submod} for N={N_submod}, s={s_submod}"
        }

    return {
        "metric_name": "mu",
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

    metric_values = [result["metric_value"] for result in results]
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric)**2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")