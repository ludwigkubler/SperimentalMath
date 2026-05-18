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
        for k in range(i+1, n):
            if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                max_row = k
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]

        # Singular or nearly singular matrix
        if matrix[i][i] == 0:
            continue

        # Normalize the current row
        for k in range(i+1, n):
            factor = matrix[k][i] / matrix[i][i]
            for j in range(i, n+1):
                matrix[k][j] -= factor * matrix[i][j]

    # Back substitution
    x = [0 for _ in range(n)]
    for i in range(n-1, -1, -1):
        x[i] = matrix[i][n] / matrix[i][i]
        for k in range(i-1, -1, -1):
            matrix[k][n] -= matrix[k][i] * x[i]
    return x

def bipartite_matching(graph):
    """Find the maximum bipartite matching using Hopcroft-Karp algorithm."""
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
                for v in graph.get(u, []):
                    if dist[pair_V[v]] == float('inf'):
                        dist[pair_V[v]] = dist[u] + 1
                        queue.append(pair_V[v])
        return dist[None] != float('inf')

    def dfs(u):
        for v in graph.get(u, []):
            if pair_V[v] is None or (dist[pair_V[v]] == dist[u] + 1 and dfs(pair_V[v])):
                pair_U[u] = v
                pair_V[v] = u
                return True
        dist[u] = float('inf')
        return False

    matching = 0
    while bfs():
        for u in U:
            if pair_U[u] is None:
                if dfs(u):
                    matching += 1
    return matching

def generate_random_dnf(n, s):
    """Generate a random monotone DNF with s terms on n variables."""
    terms = []
    for _ in range(s):
        k = random.randint(1, n)
        term = random.sample(range(n), k)
        terms.append(term)
    return terms

def generate_clique_dnf(v):
    """Generate the canonical minterm DNF for the k-CLIQUE indicator."""
    k = math.ceil(v / 2)
    n = v * (v - 1) // 2
    terms = []
    for edges in itertools.combinations(range(n), k):
        term = []
        for e in edges:
            term.append(e)
        terms.append(term)
    return terms

def compute_tau(terms, n):
    """Compute the transversal-matroid deficit τ(F)."""
    if not terms:
        return 0.0
    s = len(terms)
    graph = {}
    for i, term in enumerate(terms):
        graph[i] = term
    rho_T = bipartite_matching(graph)
    if rho_T == 0:
        return 0.0
    tau = math.log2(max(1, s / rho_T))
    return tau

def run_trial(seed):
    random.seed(seed)
    n_values = [10, 15, 20, 28, 40]
    v_values = [6, 7, 8, 9, 10]
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    instances_tested = 0

    # Test random monotone 3-DNFs (family R)
    for n in n_values:
        s_values = [n, 2*n, n**2//4]
        for s in s_values:
            if s > 1500:
                continue
            terms = generate_random_dnf(n, s)
            tau = compute_tau(terms, n)
            metric_values.append(tau)
            instances_tested += 1
            if tau > 3 * math.log2(n):
                conjecture_holds = False
                counterexample = f"Random DNF with n={n}, s={s} has τ={tau} > 3·log2(n)={3*math.log2(n)}"
                break
        if not conjecture_holds:
            break

    if conjecture_holds:
        # Test canonical CLIQUE-DNFs (family C)
        for v in v_values:
            terms = generate_clique_dnf(v)
            n = v * (v - 1) // 2
            tau = compute_tau(terms, n)
            metric_values.append(tau)
            instances_tested += 1
            if tau < (v - 3) / 4:
                conjecture_holds = False
                counterexample = f"CLIQUE-DNF with v={v} has τ={tau} < (v-3)/4={(v-3)/4}"
                break

    if conjecture_holds:
        # Test conjunction-subadditivity (i)
        for _ in range(5):
            n = random.choice(n_values)
            s1 = random.choice([n, 2*n, n**2//4])
            s2 = random.choice([n, 2*n, n**2//4])
            if s1 + s2 > 1500:
                continue
            terms1 = generate_random_dnf(n, s1)
            terms2 = generate_random_dnf(n, s2)
            tau1 = compute_tau(terms1, n)
            tau2 = compute_tau(terms2, n)
            terms_conj = [list(set(t1) | set(t2)) for t1 in terms1 for t2 in terms2]
            if len(terms_conj) > 1500:
                continue
            tau_conj = compute_tau(terms_conj, n)
            metric_values.append(tau_conj)
            instances_tested += 1
            if tau_conj > tau1 + tau2 + 1:
                conjecture_holds = False
                counterexample = f"Conjunction of two DNFs with n={n} has τ={tau_conj} > τ1+τ2+1={tau1+tau2+1}"
                break

    if not metric_values:
        return {
            "metric_name": "transversal-matroid deficit",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }

    return {
        "metric_name": "transversal-matroid deficit",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    trials = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        trials.append(trial)

    metric_values = [trial["metric_value"] for trial in trials if trial["metric_value"] is not None]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_metric_values")
        sys.exit(0)

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for trial in trials if trial["conjecture_holds"]) / len(trials)

    if all(trial["conjecture_holds"] for trial in trials):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not trial["conjecture_holds"] for trial in trials):
        first_failing_seed = next(trial["seed"] for trial in trials if not trial["conjecture_holds"])
        counterexample = next(trial["counterexample"] for trial in trials if not trial["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported")