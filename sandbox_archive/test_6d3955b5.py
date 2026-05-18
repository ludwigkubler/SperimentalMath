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

def matrix_mult(A, B):
    return [[sum(a * b for a, b in zip(row, col)) for col in zip(*B)] for row in A]

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        if matrix[i][i] == 0:
            for j in range(i + 1, n):
                if matrix[j][i] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    break
        if matrix[i][i] == 0:
            continue
        for j in range(i + 1, n):
            factor = matrix[j][i] / matrix[i][i]
            for k in range(i, n + 1):
                matrix[j][k] -= factor * matrix[i][k]
    rank = 0
    for i in range(n):
        if any(matrix[i][j] != 0 for j in range(n)):
            rank += 1
    return rank

def hopcroft_karp_bipartite_matching(graph):
    U = set(u for u, _ in graph)
    V = set(v for _, v in graph)
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
                for v in V:
                    if pair_V[v] is None:
                        dist[None] = dist[u] + 1
                    elif dist[pair_V[v]] == float('inf'):
                        dist[pair_V[v]] = dist[u] + 1
                        queue.append(pair_V[v])
        return dist[None] != float('inf')

    def dfs(u):
        if u is not None:
            for v in V:
                if pair_V[v] is None and (u, v) in graph:
                    pair_U[u] = v
                    pair_V[v] = u
                    return True
                elif dist[pair_V[v]] == dist[u] + 1 and dfs(pair_V[v]):
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

def generate_random_dnf(n, s, seed):
    random.seed(seed)
    terms = []
    for _ in range(s):
        k = random.randint(1, n)
        term = random.sample(range(n), k)
        terms.append(term)
    return terms

def generate_clique_dnf(v, seed):
    random.seed(seed)
    k = math.ceil(v / 2)
    n = v * (v - 1) // 2
    terms = []
    for _ in range(k):
        term = random.sample(range(n), k)
        terms.append(term)
    return terms

def compute_tau(terms):
    n = max(max(term) for term in terms) + 1 if terms else 0
    s = len(terms)
    if s == 0:
        return 0.0
    graph = []
    for i, term in enumerate(terms):
        for var in term:
            graph.append((i, var))
    rho = hopcroft_karp_bipartite_matching(graph)
    if rho == 0:
        return float('inf')
    tau = math.log2(max(1, s / rho))
    return tau

def run_trial(seed):
    random.seed(seed)
    n_values = [10, 15, 20, 28, 40]
    s_values = [n for n in n_values] + [2 * n for n in n_values] + [n * n // 4 for n in n_values]
    v_values = [6, 7, 8, 9, 10]

    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for s in s_values:
            if s > n * n:
                continue
            terms = generate_random_dnf(n, s, seed)
            tau = compute_tau(terms)
            metric_values.append(tau)
            if tau > 3 * math.log2(n):
                conjecture_holds = False
                counterexample = f"Random DNF with n={n}, s={s} has tau={tau} > 3*log2(n)={3*math.log2(n)}"
                break

    if not conjecture_holds:
        return {
            "metric_name": "tau",
            "metric_value": sum(metric_values) / len(metric_values) if metric_values else 0.0,
            "instances_tested": len(metric_values),
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }

    for v in v_values:
        terms = generate_clique_dnf(v, seed)
        tau = compute_tau(terms)
        metric_values.append(tau)
        if tau < (v - 3) / 4:
            conjecture_holds = False
            counterexample = f"CLIQUE DNF with v={v} has tau={tau} < (v-3)/4={(v-3)/4}"
            break

    if not conjecture_holds:
        return {
            "metric_name": "tau",
            "metric_value": sum(metric_values) / len(metric_values) if metric_values else 0.0,
            "instances_tested": len(metric_values),
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }

    for _ in range(5):
        n1 = random.choice(n_values)
        s1 = random.choice(s_values)
        terms1 = generate_random_dnf(n1, s1, seed)
        n2 = random.choice(n_values)
        s2 = random.choice(s_values)
        terms2 = generate_random_dnf(n2, s2, seed)
        terms_conjunction = [list(set(t1) | set(t2)) for t1 in terms1 for t2 in terms2]
        if len(terms_conjunction) > 1500:
            continue
        tau1 = compute_tau(terms1)
        tau2 = compute_tau(terms2)
        tau_conjunction = compute_tau(terms_conjunction)
        metric_values.append(tau_conjunction)
        if tau_conjunction > tau1 + tau2 + 1:
            conjecture_holds = False
            counterexample = f"Conjunction of two DNFs has tau={tau_conjunction} > tau1+tau2+1={tau1+tau2+1}"
            break

    return {
        "metric_name": "tau",
        "metric_value": sum(metric_values) / len(metric_values) if metric_values else 0.0,
        "instances_tested": len(metric_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]

    metric_values = []
    conjecture_holds_counts = 0
    total_instances = 0

    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        metric_values.append(trial["metric_value"])
        if trial["conjecture_holds"]:
            conjecture_holds_counts += 1
        total_instances += trial["instances_tested"]
        if not trial["conjecture_holds"]:
            print(f"RESULT: FALSIFIED counterexample=\"{trial['counterexample']}\" first_failing_seed={seed}")
            sys.exit(0)

    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0.0
    std_metric = (sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) ** 0.5 if metric_values else 0.0
    support_fraction = conjecture_holds_counts / len(seeds)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")