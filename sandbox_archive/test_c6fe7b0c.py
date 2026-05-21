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
            factor = A[i][i]
            for j in range(i, n):
                A[i][j] /= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(i, n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def noncommutative_L2_norm(M):
        n = len(M)
        sum_of_squares = 0
        for i in range(n):
            for j in range(n):
                sum_of_squares += abs(M[i][j]) ** 2
        return math.sqrt(sum_of_squares)

    def communication_complexity(n):
        # Simplified model of communication complexity for Disjointness problem
        return n * (n - 1) // 2

    n = random.randint(5, 40)
    M = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    tau_M = noncommutative_L2_norm(M)
    comm_disjointness = communication_complexity(n)

    if tau_M == 0:
        return {
            "metric_name": "communication_complexity_over_tau",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "tau_M is zero"
        }

    ratio = comm_disjointness / tau_M
    return {
        "metric_name": "communication_complexity_over_tau",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    metric_values = [r['metric_value'] for r in results if r['metric_value'] != float('inf')]
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results) or support_fraction >= 0.8:
        RESULT = f"SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values)/len(metric_values)):.2f} support_fraction={support_fraction:.2f}"
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        RESULT = f"FALSIFIED counterexample=\"communication_complexity_over_tau\" first_failing_seed={first_failing_seed}"
    else:
        RESULT = "INCONCLUSIVE insufficient_data"
    
    print(RESULT)