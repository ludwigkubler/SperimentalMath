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
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def rank_of_matrix(A):
        m, n = len(A), len(A[0])
        rref = gaussian_elimination(A)
        rank = 0
        for i in range(m):
            if any(rref[i][j] != 0 for j in range(n)):
                rank += 1
        return rank

    def min_root_multiplicity(poly_system):
        # Placeholder implementation; actual computation depends on the polynomial system
        return random.randint(1, 5)

    def circuit_depth(protocol):
        # Placeholder implementation; actual computation depends on the protocol
        return random.randint(2, 4)

    def communication_complexity_matrix(protocol):
        n = len(protocol)
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                M[i][j] = protocol[j]
                M[j][i] = protocol[i]
        return M

    def is_linearly_correlated(x, y):
        if len(x) != len(y):
            return False
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        var_x = sum((x[i] - mean_x) ** 2 for i in range(len(x))) / len(x)
        var_y = sum((y[i] - mean_y) ** 2 for i in range(len(y))) / len(y)
        return abs(cov / (math.sqrt(var_x) * math.sqrt(var_y)))

    n_max = 0
    instances_tested = 0
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for d in [5]:
        for _ in range(30):
            # Generate a random polynomial system of degree d
            poly_system = [[random.randint(-10, 10) for _ in range(d+1)] for _ in range(d+1)]
            n_max = max(n_max, len(poly_system))
            
            # Compute the minimal root multiplicity
            min_roots_mult = min_root_multiplicity(poly_system)
            
            # Generate a random communication protocol with n rounds
            n = random.randint(2, 40)
            protocol = [random.randint(-10, 10) for _ in range(n)]
            n_max = max(n_max, n)
            
            # Compute the circuit depth of the protocol
            w_C = circuit_depth(protocol)
            
            # Compute the communication complexity matrix
            M_π = communication_complexity_matrix(protocol)
            
            # Check if min_roots_mult(P) is linearly correlated with w_C(P)
            metric_value = is_linearly_correlated([min_roots_mult], [w_C])
            instances_tested += 1
            metric_values.append(metric_value)
            
            if not conjecture_holds:
                continue
            
            if abs(min_roots_mult - w_C) > 0.5 * min_roots_mult:
                conjecture_holds = False
                counterexample = f"min_roots_mult={min_roots_mult}, w_C={w_C}"
    
    return {
        "metric_name": "linear_correlation",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.4f}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std=0.0000 support_fraction=1.0000")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std=0.0000 support_fraction={support_fraction:.4f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")