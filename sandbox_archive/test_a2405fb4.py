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
    result = [[0.0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(p):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_transpose(A):
    return [list(row) for row in zip(*A)]

def matrix_trace(A):
    return sum(A[i][i] for i in range(len(A)))

def matrix_power(A, power):
    n = len(A)
    result = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        result[i][i] = 1.0
    for _ in range(power):
        result = matrix_multiply(result, A)
    return result

def matrix_eigenvalues(A):
    n = len(A)
    if n == 1:
        return [A[0][0]]
    elif n == 2:
        a = A[0][0]
        b = A[0][1]
        c = A[1][0]
        d = A[1][1]
        trace = a + d
        det = a * d - b * c
        discriminant = math.sqrt(trace**2 - 4 * det)
        return [(trace + discriminant) / 2, (trace - discriminant) / 2]
    else:
        raise ValueError("Matrix too large for this implementation")

def compute_mu(K):
    eigenvalues = matrix_eigenvalues(K)
    sum_lambda = sum(eigenvalues)
    sum_lambda_squared = sum(eigenvalue**2 for eigenvalue in eigenvalues)
    if sum_lambda_squared == 0:
        return 0.0
    return math.log2((sum_lambda**2) / sum_lambda_squared)

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
            K[i][j] = 2**(-len(F[i]) - len(F[j])) * (3/2)**intersection_size
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
    terms = []
    for term_f in F:
        for term_g in G:
            terms.append(term_f | term_g)
    return terms

def run_trial(seed):
    random.seed(seed)
    N_values = [20, 30, 40]
    v_values = [6, 7, 8, 9]
    s_values = [6, 8]

    # Family A: Upper bound
    for N in N_values:
        s = N
        F = generate_random_dnf(N, s, seed)
        K = build_gram_matrix(F)
        mu = compute_mu(K)
        bound = 4 * math.log2(2 * N + s)
        if mu > bound + 1e-9:
            return {
                "metric_name": "mu_upper_bound",
                "metric_value": mu,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"mu={mu} > bound={bound} for N={N}, s={s}"
            }

    # Family B: Lower bound
    for v in v_values:
        k = math.ceil(math.log2(v))
        F = generate_k_clique_dnf(v, k, seed)
        K = build_gram_matrix(F)
        mu = compute_mu(K)
        bound = v / 4
        if mu < bound - 1e-9:
            return {
                "metric_name": "mu_lower_bound",
                "metric_value": mu,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"mu={mu} < bound={bound} for v={v}, k={k}"
            }

    # Family C: Submodularity
    N = 20
    for s in s_values:
        F = generate_random_dnf(N, s, seed)
        G = generate_random_dnf(N, s, seed + 1)
        F_conj_G = dnf_conjunction(F, G)
        K_F = build_gram_matrix(F)
        K_G = build_gram_matrix(G)
        K_F_conj_G = build_gram_matrix(F_conj_G)
        mu_F = compute_mu(K_F)
        mu_G = compute_mu(K_G)
        mu_F_conj_G = compute_mu(K_F_conj_G)
        if mu_F_conj_G > mu_F + mu_G + 1e-9:
            return {
                "metric_name": "mu_submodularity",
                "metric_value": mu_F_conj_G,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"mu(F∧G)={mu_F_conj_G} > mu(F)+mu(G)={mu_F + mu_G} for N={N}, s={s}"
            }

    return {
        "metric_name": "mu",
        "metric_value": 0.0,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]

    metric_values = []
    conjecture_holds = []
    counterexamples = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        metric_values.append(result["metric_value"])
        conjecture_holds.append(result["conjecture_holds"])
        if not result["conjecture_holds"]:
            counterexamples.append((seed, result["counterexample"]))

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric)**2 for x in metric_values) / len(metric_values))
    support_fraction = sum(conjecture_holds) / len(conjecture_holds)

    if all(conjecture_holds):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif counterexamples:
        first_failing_seed, first_counterexample = counterexamples[0]
        print(f"RESULT: FALSIFIED counterexample=\"{first_counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")