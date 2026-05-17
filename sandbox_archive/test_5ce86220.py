# auto-injected by SEC sandbox
import collections
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
import json

def matrix_multiply(A, B):
    n = len(A)
    result = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_subtract(A, B):
    n = len(A)
    result = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = A[i][j] - B[i][j]
    return result

def jacobi_rotation(A, max_iterations=30):
    n = len(A)
    V = [[0.0 if i != j else 1.0 for j in range(n)] for i in range(n)]
    for _ in range(max_iterations):
        for p in range(n):
            for q in range(p + 1, n):
                if abs(A[p][q]) > 1e-10:
                    theta = 0.5 * math.atan2(2 * A[p][q], A[q][q] - A[p][p])
                    c = math.cos(theta)
                    s = math.sin(theta)
                    J = [[0.0 for _ in range(n)] for _ in range(n)]
                    for i in range(n):
                        J[i][i] = 1.0
                    J[p][p] = c
                    J[q][q] = c
                    J[p][q] = -s
                    J[q][p] = s
                    A = matrix_multiply(matrix_multiply(J, A), J)
                    V = matrix_multiply(V, J)
    eigenvalues = [A[i][i] for i in range(n)]
    return sorted(eigenvalues), V

def compute_laplacian(G):
    n = len(G)
    D = [[0.0 for _ in range(n)] for _ in range(n)]
    A = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        D[i][i] = sum(G[i])
        for j in range(n):
            A[i][j] = G[i][j]
    L = matrix_subtract(D, A)
    return L

def compute_capacity(eigenvalues):
    n = len(eigenvalues)
    if n < 2:
        return 0.0
    rescaled = [eigenvalues[i] / eigenvalues[-1] for i in range(n)]
    product = 1.0
    for i in range(n):
        for j in range(i + 1, n):
            product *= abs(rescaled[i] - rescaled[j])
    if product == 0.0:
        return 0.0
    return product ** (2.0 / (n * (n - 1)))

def compute_max_cut(G):
    n = len(G)
    max_cut = 0
    for mask in range(1, 1 << n):
        cut = 0
        for i in range(n):
            for j in range(i + 1, n):
                if ((mask >> i) & 1) != ((mask >> j) & 1):
                    cut += G[i][j]
        if cut > max_cut:
            max_cut = cut
    return max_cut

def generate_random_3_regular(n, seed):
    random.seed(seed)
    if n % 2 != 0:
        return None
    stubs = [i // 3 for i in range(n)]
    random.shuffle(stubs)
    G = [[0 for _ in range(n)] for _ in range(n)]
    while stubs:
        u = stubs.pop()
        v = stubs.pop()
        if u != v and G[u][v] == 0:
            G[u][v] = 1
            G[v][u] = 1
        else:
            stubs.append(u)
            stubs.append(v)
            random.shuffle(stubs)
    return G

def generate_erdos_renyi(n, p, seed):
    random.seed(seed)
    G = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < p:
                G[i][j] = 1
                G[j][i] = 1
    return G

def generate_complete_bipartite(n, seed):
    random.seed(seed)
    k = n // 2
    G = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(k):
        for j in range(k, n):
            G[i][j] = 1
            G[j][i] = 1
    return G

def generate_random_union_of_cliques(n, seed):
    random.seed(seed)
    a = random.randint(2, n - 2)
    G = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(a):
        for j in range(a):
            if i != j:
                G[i][j] = 1
    for i in range(a, n):
        for j in range(a, n):
            if i != j:
                G[i][j] = 1
    G[0][a] = 1
    G[a][0] = 1
    return G

def generate_cycle_with_chord(n, seed):
    random.seed(seed)
    G = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][(i + 1) % n] = 1
        G[(i + 1) % n][i] = 1
    u = random.randint(0, n - 1)
    v = random.randint(0, n - 1)
    if u != v and abs(u - v) != 1 and abs(u - v) != n - 1:
        G[u][v] = 1
        G[v][u] = 1
    return G

def is_connected(G):
    n = len(G)
    visited = [False] * n
    stack = [0]
    visited[0] = True
    while stack:
        u = stack.pop()
        for v in range(n):
            if G[u][v] == 1 and not visited[v]:
                visited[v] = True
                stack.append(v)
    return all(visited)

def run_trial(seed):
    random.seed(seed)
    n_values = [8, 12, 16]
    ensemble_generators = [
        generate_random_3_regular,
        generate_erdos_renyi,
        generate_complete_bipartite,
        generate_random_union_of_cliques,
        generate_cycle_with_chord
    ]
    ensemble_args = [
        (),
        (0.3,),
        (),
        (),
        ()
    ]
    results = []
    for n in n_values:
        for generator, args in zip(ensemble_generators, ensemble_args):
            for _ in range(5):
                G = generator(n, seed, *args)
                if G is None or not is_connected(G):
                    continue
                L = compute_laplacian(G)
                eigenvalues, _ = jacobi_rotation(L)
                non_trivial_eigenvalues = [e for e in eigenvalues if e > 1e-10]
                if len(non_trivial_eigenvalues) < 2:
                    continue
                cap = compute_capacity(non_trivial_eigenvalues)
                max_cut = compute_max_cut(G)
                if max_cut == 0:
                    continue
                gap = n * non_trivial_eigenvalues[-1] / (4 * max_cut) - 1
                conjecture_holds = gap <= 1.0 * cap + 0.01
                counterexample = ""
                if not conjecture_holds:
                    counterexample = f"gap={gap}, cap={cap}, eigenvalues={non_trivial_eigenvalues}, max_cut={max_cut}"
                results.append({
                    "n": n,
                    "ensemble": generator.__name__,
                    "gap": gap,
                    "cap": cap,
                    "conjecture_holds": conjecture_holds,
                    "counterexample": counterexample
                })
    metric_values = [r["gap"] - r["cap"] for r in results]
    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0.0
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0.0
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results) if results else 0.0
    counterexamples = [r["counterexample"] for r in results if not r["conjecture_holds"]]
    if counterexamples:
        return {
            "metric_name": "gap - cap",
            "metric_value": mean_metric,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": counterexamples[0]
        }
    else:
        return {
            "metric_name": "gap - cap",
            "metric_value": mean_metric,
            "instances_tested": len(results),
            "conjecture_holds": support_fraction >= 0.95,
            "counterexample": ""
        }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        result["seed"] = seed
        print(f"TRIAL: {json.dumps(result)}")
        all_results.append(result)
    metric_values = [r["metric_value"] for r in all_results]
    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0.0
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0.0
    support_fraction = sum(1 for r in all_results if r["conjecture_holds"]) / len(all_results) if all_results else 0.0
    counterexamples = [r["counterexample"] for r in all_results if not r["conjecture_holds"]]
    if counterexamples:
        print(f'RESULT: FALSIFIED counterexample="{counterexamples[0]}" first_failing_seed={all_results[0]["seed"]}')
    elif support_fraction >= 0.95:
        print(f'RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}')
    else:
        print('RESULT: INCONCLUSIVE reason=insufficient_support')