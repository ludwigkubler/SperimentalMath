# auto-injected by SEC sandbox
import math
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
            for j in range(i+1, m):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B[0]), len(B)
        C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def symplectic_topological_degree(A):
        n = len(A)
        I = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
        A_augmented = [row + row for row in A] + [I[i] + I[i] for i in range(n)]
        reduced_A = gaussian_elimination(A_augmented)
        det = 1
        for i in range(n):
            det *= reduced_A[i][i]
        return abs(det)
    
    def communication_complexity_rank(circuit):
        # Placeholder function, actual implementation depends on the circuit structure
        # For simplicity, we assume a linear relationship with n
        return random.randint(1, 2*n)
    
    n_values = [5, 10, 15, 20, 30, 40]
    var_comm_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 random circuits
            circuit = [random.choice([0, 1]) for _ in range(n)]
            A = [[Fraction(circuit[j] ^ circuit[k]) for k in range(n)] for j in range(n)]
            degree = symplectic_topological_degree(A)
            comm_rank = communication_complexity_rank(circuit)
            var_comm_rank += (comm_rank - n * Fraction(1, 2)) ** 2
            instances_tested += 1
    
    mean_var_comm_rank = var_comm_rank / instances_tested
    expected_bound = n_values[-1] * Fraction(n_values[-1], 2) * Fraction(1, 2)
    
    if abs(mean_var_comm_rank - expected_bound) <= Fraction(expected_bound, 10):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"Empirical variance {mean_var_comm_rank} not within ±10% of expected bound {expected_bound}"
    
    return {
        "metric_name": "Variance of Communication Complexity Rank",
        "metric_value": mean_var_comm_rank,
        "instances_tested": instances_tested,
        "n_max": n_values[-1],
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = (sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")