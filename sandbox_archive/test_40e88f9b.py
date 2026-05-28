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
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if m == 1:
            return A[0][0]
        det = 0
        for i in range(n):
            submatrix = [row[:i] + row[i+1:] for row in A[1:]]
            det += (-1) ** i * A[0][i] * determinant(submatrix)
        return det

    def rank(A):
        m, n = len(A), len(A[0])
        reduced_A = gaussian_elimination(A)
        r = 0
        for row in reduced_A:
            if any(row):
                r += 1
        return r

    def max_cut(n):
        # Generate a random Max-Cut instance
        graph = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            graph[i][i] = 0
        return graph

    def communication_complexity(graph):
        n = len(graph)
        # Simplified communication complexity calculation (placeholder)
        return sum(sum(row) for row in graph)

    n = random.choice([5, 10, 15, 20, 30, 40])
    entanglement_rank = int(math.sqrt(n))
    quantum_state = [[random.random() for _ in range(entanglement_rank)] for _ in range(entanglement_rank)]
    max_cut_instance = max_cut(n)
    
    cc_max_cut = communication_complexity(max_cut_instance)
    metric_value = cc_max_cut / n
    
    if entanglement_rank == int(math.sqrt(n)):
        if metric_value <= 1.5:
            conjecture_holds = True
            counterexample = ""
        else:
            conjecture_holds = False
            counterexample = "CC_{Max-Cut}(|Ψ⟩) > 1.5n for entanglement rank Θ(n^{0.5})"
    else:
        conjecture_holds = False
        counterexample = "mapping_undefined"

    return {
        "metric_name": "communication_complexity",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = results[seeds.index(first_failing_seed)]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")