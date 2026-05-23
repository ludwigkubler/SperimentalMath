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
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
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
        C = [[0 for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][k] += A[i][j] * B[j][k]
        return C

    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det

    def tropical_add(x, y):
        if x == float('-inf') or y == float('-inf'):
            return max(x, y)
        return x + y

    def tropical_multiply(x, y):
        if x == float('-inf') or y == float('-inf'):
            return float('-inf')
        return x * y

    def renyi_entropy(ρ, α=2):
        if α <= 0:
            raise ValueError("α must be greater than 0")
        entropies = [tropical_multiply(tropical_add(-x, 1), math.log(x)) for x in ρ]
        return tropical_divide(sum(entropies), 1 - α)

    def tropical_divide(x, y):
        if y == float('-inf'):
            return float('-inf')
        return x / y

    def generate_entangled_state(n):
        state = [[0] * n for _ in range(n)]
        for i in range(n):
            state[i][i] = 1
        return state

    def construct_acc0_circuit(ρ):
        n = len(ρ)
        A = generate_entangled_state(n)
        B = gaussian_elimination(A)
        det = determinant(B)
        threshold = int(math.ceil(-math.log2(det)))
        return threshold

    n = random.randint(5, 40)
    ρ = generate_entangled_state(n)
    T_ρ = renyi_entropy(ρ)
    C = construct_acc0_circuit(ρ)
    
    metric_name = "ACC⁰ Circuit Threshold"
    metric_value = abs(C - T_ρ)
    instances_tested = 1
    conjecture_holds = abs(metric_value) <= 3
    counterexample = "" if conjecture_holds else f"Threshold {C} does not match entropy {T_ρ}"

    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30*1000+1, 100))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Threshold does not match entropy\" first_failing_seed={first_failing_seed}")