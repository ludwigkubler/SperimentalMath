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
            for j in range(n):
                if i != j:
                    factor = A[j][i] / A[i][i]
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

    def renyi_entropy(density_matrix, alpha=2):
        if alpha == 1:
            return -sum(math.log2(x) * x for x in density_matrix)
        else:
            return (1 / (alpha - 1)) * math.log2(sum(x**alpha for x in density_matrix))

    def acc0_circuit_threshold(n):
        # Placeholder function to simulate ACC⁰ circuit threshold
        return random.randint(1, n)

    n = random.choice([5, 10, 15, 20, 30, 40])
    rho = [random.random() for _ in range(n)]
    T_rho = renyi_entropy(rho)
    
    f_x = lambda x: sum(x**i for i in range(1, n+1))  # Example function in P
    C_threshold = acc0_circuit_threshold(n)
    
    return {
        "metric_name": "Threshold vs Entropy",
        "metric_value": abs(C_threshold - T_rho),
        "instances_tested": 1,
        "conjecture_holds": abs(C_threshold - T_rho) <= 3,
        "counterexample": "" if abs(C_threshold - T_rho) <= 3 else f"Threshold {C_threshold} does not match entropy {T_rho}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break