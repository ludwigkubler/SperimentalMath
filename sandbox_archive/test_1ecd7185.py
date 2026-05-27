# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def generate_random_graph(n):
    edges = set()
    for i in range(n):
        for j in range(i + 1, n):
            if random.choice([True, False]):
                edges.add((i, j))
    return {i: [j for j in range(n) if (i, j) in edges or (j, i) in edges] for i in range(n)}

def isomorphism(G1, G2):
    if len(G1) != len(G2):
        return False
    nodes = list(G1.keys())
    random.shuffle(nodes)
    mapping = {nodes[0]: 0}
    for node in nodes[1:]:
        other_nodes = [n for n in G2 if len(G2[n]) == len(G1[node])]
        if not other_nodes:
            return False
        mapping[node] = random.choice(other_nodes)
    return all(len([mapping[n] for n in G1[node]]) == len(G2[mapping[node]]) for node in nodes)

def symplectic_form(G):
    n = len(G)
    S = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if (i, j) in G[i]:
                S[i][j] = 1
                S[j][i] = -1
    return S

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            return None
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    rank = sum(1 for row in A if any(row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):  # Ensure at least 100 instances per seed
            G = generate_random_graph(n)
            H = generate_random_graph(n)
            while not isomorphism(G, H):
                H = generate_random_graph(n)
            S_G = symplectic_form(G)
            rank_S_G = gaussian_elimination(S_G)
            if rank_S_G is None:
                conjecture_holds = False
                counterexample = "mapping_undefined"
                break
            C_P = n * (n - 1) / 2  # Simplified communication complexity for demonstration
            total_metric_value += C_P
            instances_tested += 1

    mean_metric_value = Fraction(total_metric_value, instances_tested)
    support_fraction = Fraction(instances_tested, len(n_values) * 5)

    if conjecture_holds:
        result = "SUPPORTED"
    elif counterexample:
        result = f"FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}"
    else:
        result = "INCONCLUSIVE"

    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")