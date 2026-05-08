# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations, permutations

def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def generate_primes(n):
    primes = []
    candidate = 2
    while len(primes) < n:
        if is_prime(candidate):
            primes.append(candidate)
        candidate += 1
    return primes

def random_triangle_free_graph(n):
    while True:
        edges = set()
        for u in range(n):
            for v in range(u + 1, n):
                if len(edges.intersection(combinations([u, v], 2))) == 0:
                    if random.choice([True, False]):
                        edges.add((u, v))
        if all(len(list(filter(lambda x: (x[0] in edge or x[1] in edge), edges))) == 3 for edge in combinations(range(n), 2)):
            return [list(edge) for edge in edges]

def max_cut(graph):
    n = len(graph)
    max_cut_value = -1
    for subset in range(1 << n):
        cut_value = sum(1 for u, v in graph if (subset & (1 << u)) != (subset & (1 << v)))
        if cut_value > max_cut_value:
            max_cut_value = cut_value
    return max_cut_value

def sdp_2(graph):
    n = len(graph)
    adjacency_matrix = [[0] * n for _ in range(n)]
    for u, v in graph:
        adjacency_matrix[u][v] = 1
        adjacency_matrix[v][u] = 1
    eigenvalues = sorted(eigenvalue_decomposition(adjacency_matrix), reverse=True)
    return len(graph) / 2 + (n / 4) * abs(eigenvalues[-1])

def permutation(matrix):
    n = len(matrix)
    perm_value = 0
    for sign in permutations(range(n)):
        product = 1
        for i, j in enumerate(sign):
            product *= matrix[i][j]
        perm_value += product
    return abs(perm_value)

def eigenvalue_decomposition(matrix):
    n = len(matrix)
    if n == 2:
        a, b, c, d = matrix[0][0], matrix[0][1], matrix[1][0], matrix[1][1]
        trace = a + d
        determinant = a * d - b * c
        lambda1 = (trace + math.sqrt(trace**2 - 4 * determinant)) / 2
        lambda2 = (trace - math.sqrt(trace**2 - 4 * determinant)) / 2
        return [lambda1, lambda2]
    else:
        for i in range(n):
            submatrix = [row[:i] + row[i+1:] for row in matrix[:i]] + [row[:i] + row[i+1:] for row in matrix[i+1:]]
            if sum(row[i] for row in matrix) == 0:
                lambda_i = -submatrix[0][0]
                submatrix[0][0] = 0
                return [lambda_i] + eigenvalue_decomposition(submatrix)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [6, 8, 10, 12, 14, 16, 18]
    pi_values = []
    gap_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(30):
            G = random_triangle_free_graph(n)
            max_cut_G = max_cut(G)
            sdp_2_G = sdp_2(G)
            perm_G = permutation(G)
            pi_G = (n / 3) * math.log2(6) - math.log2(perm_G)

            if n == 6 and G == [[0, 1, 2], [0, 3, 4], [1, 5, 2], [3, 5, 4]]:
                pi_G = 0
                gap_G = 0

            pi_values.append(pi_G * math.sqrt(n))
            gap_values.append(max_cut_G - sdp_2_G)
            instances_tested += 1

            if pi_G > 0 and max_cut_G < pi_G * math.sqrt(n) / 100:
                conjecture_holds = False
                counterexample = "pi(G) > 0 and gap(G) < pi(G) * sqrt(n) / 100"

    return {
        "metric_name": "gap",
        "metric_value": sum(gap_values) / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.6f}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")

    mean_gap = sum(result["metric_value"] for result in results) / len(results)
    std_gap = math.sqrt(sum((result["metric_value"] - mean_gap) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_gap:.6f} std={std_gap:.6f} support_fraction={support_fraction:.2f}")
    elif sum(1 for result in results if not result["conjecture_holds"]) / len(results) >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")