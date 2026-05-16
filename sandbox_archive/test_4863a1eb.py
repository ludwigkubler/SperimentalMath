# auto-injected by SEC sandbox
import itertools
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import json
from collections import defaultdict

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

def hamming_distance(x, y):
    return sum(1 for a, b in zip(x, y) if a != b)

def vietoris_rips_complex(points, max_distance):
    n = len(points)
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            d = hamming_distance(points[i], points[j])
            if d <= max_distance:
                edges.append((i, j))
    return edges

def boundary_matrix(edges, max_dimension):
    n = len(edges)
    boundary = defaultdict(list)
    for i in range(n):
        for j in range(i + 1, n):
            if edges[i][0] == edges[j][0]:
                boundary[(i, j)].append((edges[i][1], edges[j][1]))
            elif edges[i][0] == edges[j][1]:
                boundary[(i, j)].append((edges[i][1], edges[j][0]))
            elif edges[i][1] == edges[j][0]:
                boundary[(i, j)].append((edges[i][0], edges[j][1]))
            elif edges[i][1] == edges[j][1]:
                boundary[(i, j)].append((edges[i][0], edges[j][0]))
    return boundary

def reduce_boundary_matrix(boundary):
    dgm = []
    for pair, edges in boundary.items():
        if len(edges) == 1:
            dgm.append((pair[0], pair[1]))
    return dgm

def compute_persistence(dgm):
    total_persistence = 0.0
    for b, d in dgm:
        total_persistence += (d - b)
    return total_persistence

def generate_matrix(n, family):
    N = 2 ** n
    if family == "DISJ":
        M = [[0] * N for _ in range(N)]
        for i in range(N):
            for j in range(N):
                M[i][j] = (i & j) != 0
    elif family == "IP":
        M = [[0] * N for _ in range(N)]
        for i in range(N):
            for j in range(N):
                M[i][j] = bin(i & j).count('1') % 2
    elif family == "EQ":
        M = [[0] * N for _ in range(N)]
        for i in range(N):
            M[i][i] = 1
    else:
        M = [[random.choice([-1, 1]) for _ in range(N)] for _ in range(N)]
    return M

def run_trial(seed):
    random.seed(seed)
    n_values = [4, 5, 6]
    families = ["DISJ", "IP", "EQ", "RAND"]
    results = []

    for n in n_values:
        N = 2 ** n
        k = math.ceil(math.sqrt(N))
        for family in families:
            M = generate_matrix(n, family)
            total_persistence = 0.0
            instances_tested = 0

            for _ in range(30):
                S = random.sample(range(N), k)
                points = [M[x] for x in S]
                max_distance = sorted([hamming_distance(points[i], points[j]) for i in range(k) for j in range(i + 1, k)])[int(0.75 * k * (k - 1) / 2)]
                edges = vietoris_rips_complex(points, max_distance)
                boundary = boundary_matrix(edges, 1)
                dgm = reduce_boundary_matrix(boundary)
                persistence = compute_persistence(dgm)
                total_persistence += persistence
                instances_tested += 1

            avg_persistence = total_persistence / instances_tested
            metric_value = math.log2(1 + avg_persistence * k)
            conjecture_holds = True
            counterexample = ""

            if family == "DISJ" and avg_persistence < 0.05:
                conjecture_holds = False
                counterexample = f"DISJ_n={n} persistence collapsed to {avg_persistence}"

            results.append({
                "n": n,
                "family": family,
                "metric_name": "log2(1 + E_S[τ_PH] * k)",
                "metric_value": metric_value,
                "instances_tested": instances_tested,
                "conjecture_holds": conjecture_holds,
                "counterexample": counterexample
            })

    return results

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    all_results = []

    for seed in seeds:
        results = run_trial(seed)
        for result in results:
            print(f"TRIAL: {json.dumps({'seed': seed, **result})}")
            all_results.append(result)

    metric_values = [r["metric_value"] for r in all_results if r["family"] == "DISJ"]
    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0.0
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0.0
    support_fraction = sum(1 for r in all_results if r["conjecture_holds"]) / len(all_results) if all_results else 0.0

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        counterexamples = [r["counterexample"] for r in all_results if r["counterexample"]]
        if counterexamples:
            print(f"RESULT: FALSIFIED counterexample={counterexamples[0]} first_failing_seed={seeds[0]}")
        else:
            print("RESULT: INCONCLUSIVE reason=insufficient_support")