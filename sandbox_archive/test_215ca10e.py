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
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def noncommutative_l2_norm(M):
        n = len(M)
        norm = 0
        for i in range(n):
            for j in range(n):
                norm += M[i][j] ** 2
        return math.sqrt(norm)

    def communication_complexity(n):
        # Placeholder function to simulate communication complexity
        return random.randint(1, n**2)

    n = random.choice([5, 10, 15, 20, 30, 40])
    M = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    norm = noncommutative_l2_norm(M)
    comm = communication_complexity(n)
    
    if norm == 0:
        return {
            "metric_name": "communication_ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "noncommutative_l2_norm_is_zero"
        }
    
    ratio = comm / norm
    return {
        "metric_name": "communication_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio >= n**2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    metric_values = [r['metric_value'] for r in results if r['metric_value'] != float('inf')]
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values) / len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values) / len(metric_values)) ** 2 for x in metric_values) / len(metric_values)):.2f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8 and all(r['metric_value'] <= 3 for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values) / len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values) / len(metric_values)) ** 2 for x in metric_values) / len(metric_values)):.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"communication_ratio_not_sufficiently_high\" first_failing_seed={first_failing_seed}")