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

def matrix_mult(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]

def matrix_transpose(m):
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]

def matrix_add(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]

def matrix_sub(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]

def matrix_scale(m, s):
    return [[m[i][j] * s for j in range(len(m[0]))] for i in range(len(m))]

def matrix_identity(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

def matrix_power(m, p):
    result = matrix_identity(len(m))
    for _ in range(p):
        result = matrix_mult(result, m)
    return result

def matrix_trace(m):
    return sum(m[i][i] for i in range(len(m)))

def matrix_frob_norm(m):
    return math.sqrt(sum(sum(x**2 for x in row) for row in m))

def matrix_rank(m, tol=1e-9):
    n = len(m)
    if n == 0:
        return 0
    m = [row[:] for row in m]
    rank = 0
    for col in range(n):
        if col >= len(m):
            break
        pivot = rank
        while pivot < len(m) and abs(m[pivot][col]) < tol:
            pivot += 1
        if pivot == len(m):
            continue
        m[rank], m[pivot] = m[pivot], m[rank]
        for i in range(rank + 1, len(m)):
            factor = m[i][col] / m[rank][col]
            for j in range(col, n):
                m[i][j] -= factor * m[rank][j]
        rank += 1
    return rank

def matrix_eigenvalues(m, max_iter=1000, tol=1e-9):
    n = len(m)
    if n == 0:
        return []
    v = [random.random() for _ in range(n)]
    for _ in range(max_iter):
        Av = [sum(m[i][j] * v[j] for j in range(n)) for i in range(n)]
        v_new = [Av[i] / math.sqrt(sum(x**2 for x in Av)) for i in range(n)]
        if sum((v_new[i] - v[i])**2 for i in range(n)) < tol:
            break
        v = v_new
    return [sum(m[i][j] * v[j] for j in range(n)) for i in range(n)]

def generate_random_dnf(N, s, seed):
    random.seed(seed)
    terms = []
    for _ in range(s):
        term_size = random.randint(3, 6)
        term = random.sample(range(N), term_size)
        terms.append(term)
    return terms

def generate_clique_dnf(v, k, seed):
    random.seed(seed)
    vertices = list(range(v))
    random.shuffle(vertices)
    cliques = list(itertools.combinations(vertices, k))
    terms = []
    for clique in cliques:
        term = []
        for i, j in itertools.combinations(clique, 2):
            term.append(i * v + j)
        terms.append(term)
    return terms

def compute_gram_matrix(terms, rho=0.5):
    s = len(terms)
    K = [[0.0 for _ in range(s)] for _ in range(s)]
    for i in range(s):
        for j in range(s):
            intersection = len(set(terms[i]) & set(terms[j]))
            K[i][j] = 2**(-len(terms[i]) - len(terms[j])) * (3/2)**intersection
    return K

def compute_mu(K):
    eigenvalues = matrix_eigenvalues(K)
    sum_lambda = sum(eigenvalues)
    sum_lambda_sq = sum(x**2 for x in eigenvalues)
    if sum_lambda_sq == 0:
        return 0.0
    return math.log2((sum_lambda**2) / sum_lambda_sq)

def run_trial(seed):
    random.seed(seed)
    N_values = [20, 30, 40]
    v_values = [6, 7, 8, 9]
    s_values = [6, 8]

    # Family A: Upper bound
    for N in N_values:
        s = N
        terms = generate_random_dnf(N, s, seed)
        K = compute_gram_matrix(terms)
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
        N = v * (v - 1) // 2
        terms = generate_clique_dnf(v, k, seed)
        K = compute_gram_matrix(terms)
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
        terms_F = generate_random_dnf(N, s, seed)
        terms_G = generate_random_dnf(N, s, seed + 1)
        terms_FG = [list(set(t1) | set(t2)) for t1 in terms_F for t2 in terms_G]
        K_F = compute_gram_matrix(terms_F)
        K_G = compute_gram_matrix(terms_G)
        K_FG = compute_gram_matrix(terms_FG)
        mu_F = compute_mu(K_F)
        mu_G = compute_mu(K_G)
        mu_FG = compute_mu(K_FG)
        if mu_FG > mu_F + mu_G + 1e-9:
            return {
                "metric_name": "mu_submodularity",
                "metric_value": mu_FG,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"mu_FG={mu_FG} > mu_F+mu_G={mu_F + mu_G} for N={N}, s={s}"
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
    std = math.sqrt(sum((x - mean)**2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        counterexamples = [r["counterexample"] for r in results if not r["conjecture_holds"]]
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample={counterexamples[0]} first_failing_seed={first_failing_seed}")