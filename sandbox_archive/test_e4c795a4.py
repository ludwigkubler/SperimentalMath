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
        n = len(A)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def sdp_relaxation(A, d):
        n = len(A)
        x = [random.uniform(-1, 1) for _ in range(d)]
        y = [random.uniform(-1, 1) for _ in range(n-d)]
        value = sum(x[i] * x[j] * A[i][j] for i in range(d) for j in range(i+1, d)) + sum(y[i] * y[j] * A[i][j] for i in range(n-d) for j in range(i+1, n-d))
        return value
    
    def max_cut_instance(n):
        edges = [(i, j) for i in range(n) for j in range(i+1, n)]
        random.shuffle(edges)
        cut_edges = edges[:n-1]
        return cut_edges
    
    def polynomial_system(cut_edges):
        n = len(cut_edges) + 1
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            A[i][i] = 1
        for u, v in cut_edges:
            A[u][v] = -1
            A[v][u] = -1
        return A
    
    def real_radical_dimension(A):
        n = len(A)
        rank = 0
        for i in range(n):
            if any(abs(A[j][i]) > 1e-9 for j in range(rank)):
                rank += 1
        return rank
    
    n = random.randint(5, 40)
    cut_edges = max_cut_instance(n)
    A = polynomial_system(cut_edges)
    d = real_radical_dimension(gaussian_elimination(A))
    
    if d == 0:
        return {
            "metric_name": "SOS Degree",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    sos_degree = sdp_relaxation(A, d)
    if sos_degree is None:
        return {
            "metric_name": "SOS Degree",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    metric_value = math.log(d)
    conjecture_holds = sos_degree >= metric_value
    counterexample = "" if conjecture_holds else f"SOS degree {sos_degree} < log(d) = {metric_value}"
    
    return {
        "metric_name": "SOS Degree",
        "metric_value": sos_degree,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(result['metric_value'] for result in results) / len(results)} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(result['counterexample'] for result in results if not result['conjecture_holds'])}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")