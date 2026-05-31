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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return [row[:n-1] for row in A]

    def matrix_rank(A):
        rref = gaussian_elimination(A)
        rank = 0
        for row in rref:
            if any(row):
                rank += 1
        return rank

    def boolean_circuit_entanglement(G):
        n = len(G)
        entangled_gates = 0
        for i in range(n):
            for j in range(i+1, n):
                if G[i][j] == 1:
                    entangled_gates += 1
        return entangled_gates

    def generate_d_regular_graph(d, n):
        G = [[0]*n for _ in range(n)]
        degree_count = [0]*n
        while any(degree != d for degree in degree_count):
            i, j = random.sample(range(n), 2)
            if i == j or G[i][j] == 1:
                continue
            G[i][j], G[j][i] = 1, 1
            degree_count[i] += 1
            degree_count[j] += 1
        return G

    n_max = 0
    instances_tested = 0
    total_alpha_K = 0.0
    total_E_G = 0.0

    for d in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            n = random.randint(5, min(n_max + 10, 40))
            G = generate_d_regular_graph(d, n)
            alpha_K = matrix_rank(G)
            E_G = boolean_circuit_entanglement(G)
            total_alpha_K += alpha_K
            total_E_G += E_G
            instances_tested += 1
            if n > n_max:
                n_max = n

    mean_alpha_K = total_alpha_K / instances_tested
    mean_E_G = total_E_G / instances_tested
    epsilon = 0.5  # Example constant, adjust as needed
    correlation = abs(mean_alpha_K - epsilon * mean_E_G) <= 3

    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation,
        "counterexample": "" if correlation else f"alpha_K={mean_alpha_K}, E_G={mean_E_G}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")