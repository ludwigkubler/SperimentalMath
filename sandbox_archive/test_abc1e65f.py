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
            max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            for j in range(m):
                if i != j:
                    factor = -A[j][i]
                    for k in range(n):
                        A[j][k] += factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    def lcm(a, b):
        return abs(a * b) // gcd(a, b)

    def is_cusp_form(A):
        m, n = len(A), len(A[0])
        if m != n or A[0][0] == 0:
            return False
        for i in range(1, m):
            if A[i][i] == 0 or any(A[j][k] != 0 for j in range(i) for k in range(n)):
                return False
        return True

    def minimal_level(m):
        n = max(5, min(40, int(math.ceil(m ** (1/3)))))
        while True:
            A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
            A[0][0] = 1
            if is_cusp_form(gaussian_elimination(A)):
                return n

    m_values = [5, 10, 15, 20, 30, 40]
    L_values = []
    
    for m in m_values:
        for _ in range(5):
            L = minimal_level(m)
            if L is None:
                return {
                    "metric_name": "L",
                    "metric_value": float('inf'),
                    "instances_tested": 1,
                    "n_max": m,
                    "conjecture_holds": False,
                    "counterexample": "mapping_undefined"
                }
            L_values.append(L)
    
    mean_L = sum(L_values) / len(L_values)
    std_L = math.sqrt(sum((x - mean_L) ** 2 for x in L_values) / len(L_values))
    support_fraction = sum(0.8 * m ** (1/3) <= L <= 1.2 * m ** (1/3) for L, m in zip(L_values, m_values)) / len(m_values)
    
    return {
        "metric_name": "L",
        "metric_value": mean_L,
        "instances_tested": len(L_values),
        "n_max": max(m_values),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_L = sum(r['metric_value'] for r in results) / len(results)
    std_L = math.sqrt(sum((r['metric_value'] - mean_L) ** 2 for r in results) / len(results))
    support_fraction = sum(0.8 * m ** (1/3) <= L <= 1.2 * m ** (1/3) for L, m in zip([r['metric_value'] for r in results], [r['n_max'] for r in results])) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_L} std={std_L} support_fraction={support_fraction}")
    elif any(L > 1.2 * m ** (1/3) or L < 0.8 * m ** (1/3) for L, m in zip([r['metric_value'] for r in results], [r['n_max'] for r in results])):
        first_failing_seed = next(seed for seed, result in enumerate(results) if any(L > 1.2 * m ** (1/3) or L < 0.8 * m ** (1/3) for L, m in zip([result], [r['n_max'] for r in results])))
        print(f"RESULT: FALSIFIED counterexample=\"L out of bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")