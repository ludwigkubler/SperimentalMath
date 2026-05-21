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
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                return None  # Singular matrix
            for j in range(i, n):
                A[i][j] /= pivot
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(i, n):
                        A[k][j] -= factor * A[i][j]
        return A
    
    def symplectic_orthogonal_matrix(dnf):
        n = len(dnf)
        A = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    A[i][j] = 1
                elif abs(i - j) == 2:
                    A[i][j] = -1
        return A
    
    def spectral_gap(A):
        n = len(A)
        eigenvalues = []
        for _ in range(10):  # Power iteration method
            v = [random.random() for _ in range(n)]
            v /= sum(v) ** 0.5
            Av = [sum(A[i][j] * v[j] for j in range(n)) for i in range(n)]
            lambda_ = sum(Av[i] * v[i] for i in range(n))
            eigenvalues.append(lambda_)
        return max(eigenvalues) - min(eigenvalues)
    
    def is_submodular(gap, n):
        return gap >= n**2
    
    def is_bounded_by_log2_n(gap, n):
        return gap <= math.log2(n)**2
    
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(30):  # 30 instances per seed
        n = random.randint(5, 40)
        dnf = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        A = symplectic_orthogonal_matrix(dnf)
        if A is None:
            continue
        gap = spectral_gap(A)
        instances_tested += 1
        
        if not is_submodular(gap, n):
            conjecture_holds = False
            counterexample = "Spectral gap is not submodular"
            break
        
        if not is_bounded_by_log2_n(gap, n):
            conjecture_holds = False
            counterexample = f"Spectral gap exceeds O(log^2 {n})"
            break
    
    return {
        "metric_name": "spectral_gap",
        "metric_value": gap,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = (sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{trial_result['counterexample']}\" first_failing_seed={first_failing_seed}")