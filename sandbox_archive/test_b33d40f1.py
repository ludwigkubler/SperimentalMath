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
from collections import deque

def matrix_multiply(A, B):
    """Multiply two matrices A and B."""
    if len(A[0]) != len(B):
        raise ValueError("Incompatible matrix dimensions")
    result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def gaussian_elimination(matrix):
    """Perform Gaussian elimination on a matrix."""
    n = len(matrix)
    for i in range(n):
        # Partial pivoting
        max_row = i
        for k in range(i + 1, n):
            if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                max_row = k
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]

        # Singular matrix
        if matrix[i][i] == 0:
            continue

        # Normalize the pivot row
        pivot = matrix[i][i]
        for j in range(i, n + 1):
            matrix[i][j] /= pivot

        # Eliminate other rows
        for k in range(n):
            if k != i and matrix[k][i] != 0:
                factor = matrix[k][i]
                for j in range(i, n + 1):
                    matrix[k][j] -= factor * matrix[i][j]
    return matrix

def rank(matrix):
    """Compute the rank of a matrix."""
    if not matrix:
        return 0
    m = len(matrix)
    n = len(matrix[0])
    if m == 0 or n == 0:
        return 0
    rank = 0
    for row in matrix:
        if any(row):
            rank += 1
    return rank

def hopcroft_karp(graph):
    """Compute the maximum matching in a bipartite graph using Hopcroft-Karp algorithm."""
    U = set(graph.keys())
    V = set()
    for neighbors in graph.values():
        V.update(neighbors)
    pair_U = {u: None for u in U}
    pair_V = {v: None for v in V}
    dist = {}

    def bfs():
        queue = deque()
        for u in U:
            if pair_U[u] is None:
                dist[u] = 0
                queue.append(u)
            else:
                dist[u] = float('inf')
        dist[None] = float('inf')
        while queue:
            u = queue.popleft()
            if dist[u] < dist[None]:
                for v in graph.get(u, set()):
                    if dist[pair_V[v]] == float('inf'):
                        dist[pair_V[v]] = dist[u] + 1
                        queue.append(pair_V[v])
        return dist[None] != float('inf')

    def dfs(u):
        if u is not None:
            for v in graph.get(u, set()):
                if dist[pair_V[v]] == dist[u] + 1:
                    if dfs(pair_V[v]):
                        pair_U[u] = v
                        pair_V[v] = u
                        return True
            dist[u] = float('inf')
            return False
        return True

    matching = 0
    while bfs():
        for u in U:
            if pair_U[u] is None:
                if dfs(u):
                    matching += 1
    return matching

def generate_random_dnf(n, s, k):
    """Generate a random monotone DNF with s terms, each of size k."""
    terms = []
    for _ in range(s):
        term = random.sample(range(n), k)
        terms.append(set(term))
    return terms

def generate_clique_dnf(v, k):
    """Generate the canonical minterm DNF for the k-CLIQUE indicator on K_v."""
    n = v * (v - 1) // 2
    edges = list(itertools.combinations(range(v), 2))
    terms = []
    for clique in itertools.combinations(range(v), k):
        term = set()
        for i, j in itertools.combinations(clique, 2):
            term.add(edges.index((i, j)))
        terms.append(term)
    return terms

def compute_tau(terms, n):
    """Compute the transversal-matroid deficit τ(F)."""
    if not terms:
        return 0.0
    graph = {i: set() for i in range(len(terms))}
    for i, term in enumerate(terms):
        for var in term:
            graph[i].add(var)
    rho = hopcroft_karp(graph)
    s = len(terms)
    if rho == 0:
        return float('inf')
    tau = math.log2(max(1, s / rho))
    return tau

def run_trial(seed):
    random.seed(seed)
    n_values = [10, 15, 20, 28, 40]
    s_values = [lambda n: n, lambda n: 2 * n, lambda n: n * n // 4]
    v_values = [6, 7, 8, 9, 10]

    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    # Test random monotone 3-DNFs
    for n in n_values:
        for s_func in s_values:
            s = s_func(n)
            if s > 1500:
                continue
            terms = generate_random_dnf(n, s, 3)
            tau = compute_tau(terms, n)
            metric_values.append(tau)
            instances_tested += 1
            if tau > 3 * math.log2(n):
                conjecture_holds = False
                counterexample = f"Random DNF with n={n}, s={s} has τ={tau} > 3·log2(n)={3 * math.log2(n)}"
                break
        if not conjecture_holds:
            break

    if conjecture_holds:
        # Test canonical CLIQUE-DNFs
        for v in v_values:
            k = v // 2 + (v % 2)
            terms = generate_clique_dnf(v, k)
            n = v * (v - 1) // 2
            tau = compute_tau(terms, n)
            metric_values.append(tau)
            instances_tested += 1
            if tau < (v - 3) / 4:
                conjecture_holds = False
                counterexample = f"CLIQUE-DNF with v={v} has τ={tau} < (v-3)/4={(v-3)/4}"
                break

    if conjecture_holds:
        # Test conjunction-subadditivity
        for _ in range(5):
            n = random.choice(n_values)
            s1 = random.choice([n, 2 * n, n * n // 4])
            s2 = random.choice([n, 2 * n, n * n // 4])
            if s1 + s2 > 1500:
                continue
            terms1 = generate_random_dnf(n, s1, 3)
            terms2 = generate_random_dnf(n, s2, 3)
            tau1 = compute_tau(terms1, n)
            tau2 = compute_tau(terms2, n)
            terms_conj = [t1.union(t2) for t1 in terms1 for t2 in terms2]
            tau_conj = compute_tau(terms_conj, n)
            metric_values.append(tau_conj)
            instances_tested += 1
            if tau_conj > tau1 + tau2 + 1:
                conjecture_holds = False
                counterexample = f"Conjunction of two DNFs with n={n} has τ={tau_conj} > τ1+τ2+1={tau1 + tau2 + 1}"
                break

    if not metric_values:
        return {
            "metric_name": "tau",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No instances tested"
        }

    mean_metric = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "tau",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(1, 1000000) for _ in range(30)]
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

    if all(trial["conjecture_holds"] for trial in trials):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not trial["conjecture_holds"] for trial in trials):
        first_failing_seed = seeds[next(i for i, trial in enumerate(trials) if not trial["conjecture_holds"])]
        counterexample = trials[next(i for i, trial in enumerate(trials) if not trial["conjecture_holds"])]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")