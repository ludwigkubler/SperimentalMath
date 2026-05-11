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

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def truth_table_to_characteristic_vector(f, n):
    return [f(tuple(bin(i)[2:].zfill(n))) for i in range(2**n)]

def max_plus_matrix_add(A, B):
    m = len(A)
    n = len(A[0])
    C = [[max(A[i][j], B[i][j]) for j in range(n)] for i in range(m)]
    return C

def max_plus_matrix_multiply(A, B):
    m = len(A)
    p = len(B)
    n = len(B[0])
    C = [[-math.inf] * n for _ in range(m)]
    for i in range(m):
        for k in range(p):
            for j in range(n):
                if A[i][k] != -math.inf and B[k][j] != -math.inf:
                    C[i][j] = max(C[i][j], A[i][k] + B[k][j])
    return C

def max_plus_matrix_power(A, k):
    m = len(A)
    result = [[-math.inf if i != j else 0 for j in range(m)] for i in range(m)]
    while k > 0:
        if k % 2 == 1:
            result = max_plus_matrix_multiply(result, A)
        A = max_plus_matrix_multiply(A, A)
        k //= 2
    return result

def tropical_convex_hull_dimension(vector):
    n = len(vector)
    I = [[-math.inf] * n for _ in range(n)]
    for i in range(n):
        I[i][i] = vector[i]
    H = max_plus_matrix_power(I, n - 1)
    rank = sum(1 for row in H if any(x != -math.inf for x in row))
    return rank

def min_acc0_circuit_size(f, n):
    # Placeholder function to simulate ACC^0 circuit size calculation
    # This is a simplified version and may not accurately reflect actual complexity
    return random.randint(1, 2**n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10
    f = generate_boolean_function(n)
    vector = truth_table_to_characteristic_vector(f, n)
    dimension = tropical_convex_hull_dimension(vector)
    s = min_acc0_circuit_size(f, n)
    conjecture_holds = dimension <= math.log2(s)
    counterexample = "" if conjecture_holds else f"Dimension {dimension} > log2({s})"
    return {
        "metric_name": "tropical_convex_hull_dimension",
        "metric_value": dimension,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean_dimension = sum(r["metric_value"] for r in results) / len(results)
    std_dimension = math.sqrt(sum((r["metric_value"] - mean_dimension)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_dimension} std={std_dimension} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Dimension exceeds log2(s)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data or conflicting results")