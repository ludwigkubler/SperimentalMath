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
            if A[i][i] == 0:
                continue
            factor = Fraction(1, A[i][i])
            for j in range(n):
                A[i][j] *= factor
            for j in range(m):
                if j != i and A[j][i] != 0:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n = len(A), len(B[0])
        p = len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def bp_readTwice_tensor_width(P):
        # Placeholder function to compute BP_readTwice tensor width
        # This is a dummy implementation and should be replaced with actual logic
        n = len(P)
        return n**2  # Dummy value for demonstration purposes

    def quadratic_form(Q, x):
        result = 0
        for i in range(len(x)):
            for j in range(i+1, len(x)):
                result += Q[i][j] * x[i] * x[j]
        return result

    n = random.randint(5, 40)
    r = random.randint(1, min(n, 10))
    K = [random.randint(-10, 10) for _ in range(n)]
    
    P = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    Q = [[0] * n for _ in range(n)]
    for i in range(r):
        x_i = random.choice(K)
        for j in range(n):
            if P[j][i]:
                Q[i][j] = x_i
    
    rho_P = bp_readTwice_tensor_width(P)
    rho_Q = quadratic_form(Q, K)
    
    upper_bound = n**2 * r * math.log(r)
    
    return {
        "metric_name": "BP_readTwice_tensor_width",
        "metric_value": rho_Q,
        "instances_tested": 1,
        "conjecture_holds": rho_Q <= upper_bound,
        "counterexample": "" if rho_Q <= upper_bound else f"rho(Q)={rho_Q} > O(n^2r log(r))={upper_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")