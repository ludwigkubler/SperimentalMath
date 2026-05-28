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
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def generate_primes(k):
        primes = []
        num = 2
        while len(primes) < k:
            if is_prime(num):
                primes.append(num)
            num += 1
        return primes
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0.0] * n
        for i in range(n - 1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
        return x
    
    def matrix_multiply(A, B):
        m = len(A)
        n = len(B[0])
        p = len(B)
        C = [[0.0 for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        sign = 1
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += sign * A[0][j] * determinant(submatrix)
            sign *= -1
        return det
    
    def generate_ac0_circuit(n, func):
        if n == 1:
            return [func]
        else:
            left = generate_ac0_circuit(n // 2, lambda x: x[0])
            right = generate_ac0_circuit(n // 2, lambda x: x[1])
            return [(left[i], right[i]) for i in range(len(left))]
    
    def count_irreducible_components(circuit):
        if not circuit:
            return 0
        n = len(circuit)
        A = [[0.0] * (n + 1) for _ in range(n + 1)]
        b = [0.0] * (n + 1)
        for i in range(n):
            A[i][i] = 1.0
            b[i] = circuit[i]
        A[n][n] = 1.0
        x = gaussian_elimination(A, b)
        components = set()
        for i in range(n):
            if x[i] != 0:
                components.add(i)
        return len(components)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_components = 0
    num_trials = 0
    
    for n in n_values:
        circuit = generate_ac0_circuit(n, lambda x: x[0] ^ x[1])
        components = count_irreducible_components(circuit)
        total_components += components
        num_trials += 1
    
    mean_components = total_components / num_trials
    std_components = math.sqrt(sum((components - mean_components) ** 2 for components in range(total_components)) / num_trials)
    
    conjecture_holds = mean_components < 0.5 * math.log(num_trials)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "irreducible_components",
        "metric_value": mean_components,
        "instances_tested": num_trials,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else generate_primes(30)
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_components = sum(result["metric_value"] for result in results) / len(results)
    std_components = math.sqrt(sum((result["metric_value"] - mean_components) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_components} std={std_components} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_components} std={std_components} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")