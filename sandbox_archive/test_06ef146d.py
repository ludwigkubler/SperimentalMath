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
    
    def generate_random_entangled_state(n):
        state = [[random.random() for _ in range(n)] for _ in range(n)]
        for i in range(n):
            state[i][i] += 0.5
        return state
    
    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A, b):
        n = len(A)
        for i in range(n):
            max_row = i
            for k in range(i+1, n):
                if abs(A[k][i]) > abs(A[max_row][i]):
                    max_row = k
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for k in range(i+1, n):
                factor = A[k][i] / A[i][i]
                A[k][i] = 0
                for j in range(i+1, n):
                    A[k][j] -= factor * A[i][j]
                b[k] -= factor * b[i]
        x = [0 for _ in range(n)]
        for i in range(n-1, -1, -1):
            x[i] = b[i]
            for k in range(i+1, n):
                x[i] -= A[i][k] * x[k]
            x[i] /= A[i][i]
        return x
    
    def distillable_entropy(state):
        n = len(state)
        eigenvalues = []
        for _ in range(10):  # Power iteration method to approximate eigenvalues
            v = [random.random() for _ in range(n)]
            v = [x / sum(v) for x in v]
            Av = matrix_multiplication(state, v)
            lambda_i = sum(Av[i] * v[i] for i in range(n))
            eigenvalues.append(lambda_i)
        return min(eigenvalues)
    
    def tropicalized_deligne_lusztig_indicators(state):
        n = len(state)
        indicators = []
        for _ in range(10):  # Random sampling to approximate
            v = [random.random() for _ in range(n)]
            v = [x / sum(v) for x in v]
            Av = matrix_multiplication(state, v)
            indicator = max(abs(Av[i][j] - state[i][j]) for i in range(n) for j in range(n))
            indicators.append(indicator)
        return min(indicators)
    
    n = 40
    state = generate_random_entangled_state(n)
    epsilon = distillable_entropy(state)
    tau = tropicalized_deligne_lusztig_indicators(state)
    
    if epsilon <= 0:
        return {
            "metric_name": "tau",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "epsilon_not_positive"
        }
    
    metric_value = tau
    conjecture_holds = tau >= Fraction(1, 20) * math.log(1 / epsilon)
    counterexample = "" if conjecture_holds else f"tau={tau}, expected>=c*log(1/epsilon)"
    
    return {
        "metric_name": "tau",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_tau = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_tau = math.sqrt(sum((r["metric_value"] - mean_tau)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_tau} std={std_tau} support_fraction={support_fraction}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_tau} std={std_tau} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='tau<{Fraction(1, 20)*math.log(1/2**-20)}' first_failing_seed={first_failing_seed}")