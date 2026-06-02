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
    
    def generate_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def characteristic_function(circuit, x):
        return circuit[x]
    
    def gaussian_elimination(A, b):
        n = len(b)
        A_augmented = [[A[i][j] for j in range(n)] + [b[i]] for i in range(n)]
        for i in range(n):
            max_row = max(range(i, n), key=lambda k: abs(A_augmented[k][i]))
            A_augmented[i], A_augmented[max_row] = A_augmented[max_row], A_augmented[i]
            factor = A_augmented[i][i]
            A_augmented[i] = [x / factor for x in A_augmented[i]]
            for j in range(n):
                if i != j:
                    factor = A_augmented[j][i]
                    A_augmented[j] = [A_augmented[j][k] - factor * A_augmented[i][k] for k in range(n + 1)]
        return [row[-1] for row in A_augmented]
    
    def communication_complexity_rank(circuit):
        n = len(circuit)
        A = [[0] * (2**n) for _ in range(2**n)]
        b = [0] * (2**n)
        for i in range(2**n):
            for j in range(2**n):
                if characteristic_function(circuit, i) == characteristic_function(circuit, j):
                    A[i][j] = 1
                else:
                    A[i][j] = -1
                b[i] += A[i][j]
        return len(gaussian_elimination(A, b))
    
    def minimal_local_indefinite_integral(circuit):
        n = len(circuit)
        integral = 0
        for i in range(2**n):
            integral += characteristic_function(circuit, i) * math.log2(i + 1)
        return integral
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_circuit(n)
            lii = minimal_local_indefinite_integral(circuit)
            rank = communication_complexity_rank(circuit)
            results.append((lii, rank))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    n_max = max(n_values)
    instances_tested = len(results)
    correlation = sum(x * y for x, y in results) / (sum(x**2 for x, _ in results) ** 0.5 * sum(y**2 for _, y in results) ** 0.5)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}")