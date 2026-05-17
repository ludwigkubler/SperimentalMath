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

def is_subset(a, b):
    return all(x in b for x in a)

def is_antichain(antichain):
    for a, b in itertools.combinations(antichain, 2):
        if is_subset(a, b) or is_subset(b, a):
            return False
    return True

def generate_random_antichain(n, k):
    antichain = []
    for _ in range(k):
        while True:
            candidate = frozenset(random.sample(range(n), random.randint(1, n)))
            if all(not is_subset(candidate, a) and not is_subset(a, candidate) for a in antichain):
                antichain.append(candidate)
                break
    return antichain

def compute_minterms_and_maxterms(f):
    minterms = []
    maxterms = []
    n = len(next(iter(f))) if f else 0
    for bits in itertools.product([0, 1], repeat=n):
        if all(is_subset(m, bits) for m in f):
            minterms.append(frozenset(bits))
        if not any(is_subset(bits, k) for k in f):
            maxterms.append(frozenset(bits))
    return minterms, maxterms

def build_bipartite_graph(minterms, maxterms):
    graph = {}
    for m in minterms:
        for k in maxterms:
            edge = (m, k)
            weight = len(m & k)
            if edge in graph:
                graph[edge] += weight
            else:
                graph[edge] = weight
    return graph

def compute_reduced_laplacian(graph, minterms, maxterms):
    n = len(minterms) + len(maxterms) + 1
    laplacian = [[0] * n for _ in range(n)]
    for i, m in enumerate(minterms):
        for j, k in enumerate(maxterms):
            edge = (m, k)
            if edge in graph:
                laplacian[i][j + len(minterms)] = -graph[edge]
                laplacian[j + len(minterms)][i] = -graph[edge]
                laplacian[i][i] += graph[edge]
                laplacian[j + len(minterms)][j + len(minterms)] += graph[edge]
    for j in range(len(maxterms)):
        laplacian[len(minterms) + len(maxterms)][len(minterms) + j] = -1
        laplacian[len(minterms) + j][len(minterms) + len(maxterms)] = -1
        laplacian[len(minterms) + len(maxterms)][len(minterms) + len(maxterms)] += 1
        laplacian[len(minterms) + j][len(minterms) + j] += 1
    return laplacian

def matrix_determinant(matrix):
    n = len(matrix)
    det = 1
    for i in range(n):
        if matrix[i][i] == 0:
            for j in range(i + 1, n):
                if matrix[j][i] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    det *= -1
                    break
            else:
                return 0
        pivot = matrix[i][i]
        det *= pivot
        for j in range(i + 1, n):
            factor = Fraction(matrix[j][i], pivot)
            for k in range(i, n):
                matrix[j][k] -= factor * matrix[i][k]
    return det

def compute_spanning_trees(laplacian):
    n = len(laplacian)
    if n == 0:
        return 0
    reduced_laplacian = [row[:n-1] for row in laplacian[:n-1]]
    det = matrix_determinant(reduced_laplacian)
    return det

def compute_sigma(tau):
    return math.log2(1 + tau)

def compute_dkw(f, minterms, maxterms):
    if not f:
        return 0
    n = len(next(iter(f)))
    max_depth = 0
    for m in minterms:
        for k in maxterms:
            if not is_subset(m, k):
                continue
            depth = 0
            current = m
            while current != k:
                for i in range(n):
                    if i in current and i not in k:
                        new_current = current - {i}
                        if is_subset(new_current, k):
                            current = new_current
                            depth += 1
                            break
            max_depth = max(max_depth, depth)
    return max_depth

def run_trial(seed):
    random.seed(seed)
    n = random.choice([4, 5, 6, 7, 8])
    k = random.randint(2, 6)
    f = generate_random_antichain(n, k)
    minterms, maxterms = compute_minterms_and_maxterms(f)
    graph = build_bipartite_graph(minterms, maxterms)
    laplacian = compute_reduced_laplacian(graph, minterms, maxterms)
    tau = compute_spanning_trees(laplacian)
    sigma = compute_sigma(tau)
    dkw = compute_dkw(f, minterms, maxterms)
    bound = dkw * (len(minterms) + len(maxterms) + 1) * math.log2(n + 2)
    conjecture_holds = sigma <= bound
    counterexample = "" if conjecture_holds else f"sigma={sigma} > bound={bound} for n={n}, k={k}"
    return {
        "metric_name": "sigma_bound_ratio",
        "metric_value": sigma / bound if bound != 0 else 0,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def run_fixed_benchmarks():
    benchmarks = {
        "THR_2^5": (5, [{0, 1}, {0, 2}, {0, 3}, {0, 4}]),
        "THR_3^6": (6, [{0, 1, 2}, {0, 1, 3}, {0, 1, 4}, {0, 1, 5}, {0, 2, 3}, {0, 2, 4}, {0, 2, 5}, {0, 3, 4}, {0, 3, 5}, {0, 4, 5}]),
        "MAJ_5": (5, [{0, 1, 2}, {0, 1, 3}, {0, 1, 4}, {0, 2, 3}, {0, 2, 4}, {0, 3, 4}, {1, 2, 3}, {1, 2, 4}, {1, 3, 4}, {2, 3, 4}]),
        "MAJ_7": (7, [{0, 1, 2, 3}, {0, 1, 2, 4}, {0, 1, 2, 5}, {0, 1, 2, 6}, {0, 1, 3, 4}, {0, 1, 3, 5}, {0, 1, 3, 6}, {0, 1, 4, 5}, {0, 1, 4, 6}, {0, 1, 5, 6}, {0, 2, 3, 4}, {0, 2, 3, 5}, {0, 2, 3, 6}, {0, 2, 4, 5}, {0, 2, 4, 6}, {0, 2, 5, 6}, {0, 3, 4, 5}, {0, 3, 4, 6}, {0, 3, 5, 6}, {0, 4, 5, 6}, {1, 2, 3, 4}, {1, 2, 3, 5}, {1, 2, 3, 6}, {1, 2, 4, 5}, {1, 2, 4, 6}, {1, 2, 5, 6}, {1, 3, 4, 5}, {1, 3, 4, 6}, {1, 3, 5, 6}, {1, 4, 5, 6}, {2, 3, 4, 5}, {2, 3, 4, 6}, {2, 3, 5, 6}, {2, 4, 5, 6}, {3, 4, 5, 6}]),
        "PM_{3,3}": (6, [{0, 1}, {0, 2}, {0, 3}, {1, 4}, {1, 5}, {2, 4}, {2, 5}, {3, 4}, {3, 5}])
    }
    results = []
    for name, (n, f) in benchmarks.items():
        minterms, maxterms = compute_minterms_and_maxterms(f)
        graph = build_bipartite_graph(minterms, maxterms)
        laplacian = compute_reduced_laplacian(graph, minterms, maxterms)
        tau = compute_spanning_trees(laplacian)
        sigma = compute_sigma(tau)
        dkw = compute_dkw(f, minterms, maxterms)
        bound = dkw * (len(minterms) + len(maxterms) + 1) * math.log2(n + 2)
        conjecture_holds = sigma <= bound
        counterexample = "" if conjecture_holds else f"sigma={sigma} > bound={bound} for benchmark {name}"
        results.append({
            "metric_name": "sigma_bound_ratio",
            "metric_value": sigma / bound if bound != 0 else 0,
            "instances_tested": 1,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    return results

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    trials = []
    for seed in seeds:
        trial = run_trial(seed)
        trial["seed"] = seed
        print(f"TRIAL: {trial}")
        trials.append(trial)
    benchmark_results = run_fixed_benchmarks()
    for i, result in enumerate(benchmark_results):
        result["seed"] = f"benchmark_{i}"
        print(f"TRIAL: {result}")
        trials.extend(benchmark_results)
    metric_values = [trial["metric_value"] for trial in trials]
    mean = sum(metric_values) / len(metric_values) if metric_values else 0
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0
    support_fraction = sum(1 for trial in trials if trial["conjecture_holds"]) / len(trials) if trials else 0
    if all(trial["conjecture_holds"] for trial in trials):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        for trial in trials:
            if not trial["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{trial['counterexample']}\" first_failing_seed={trial['seed']}")
                break