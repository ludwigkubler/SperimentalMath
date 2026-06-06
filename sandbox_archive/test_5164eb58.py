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
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

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

    def lefschetz_number(A):
        return abs(determinant(gaussian_elimination(A)))

    def circuit_entanglement(phi):
        # Placeholder function for circuit entanglement calculation
        # This is a dummy implementation and should be replaced with actual logic
        return random.random()

    n = 40
    instances_tested = 30
    L_values = []
    epsilon_values = []

    for _ in range(instances_tested):
        phi = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        L = lefschetz_number(phi)
        epsilon = circuit_entanglement(phi)
        L_values.append(L)
        epsilon_values.append(epsilon)

    correlation_coefficient = sum((L - sum(L_values) / instances_tested) * (epsilon - sum(epsilon_values) / instances_tested) for L, epsilon in zip(L_values, epsilon_values)) / ((instances_tested - 1) * math.sqrt(sum((L - sum(L_values) / instances_tested) ** 2 for L in L_values)) * math.sqrt(sum((epsilon - sum(epsilon_values) / instances_tested) ** 2 for epsilon in epsilon_values)))

    mean_absolute_difference = sum(abs(L - (sum(epsilon_values) / instances_tested) * epsilon) for L, epsilon in zip(L_values, epsilon_values)) / instances_tested

    conjecture_holds = correlation_coefficient >= 0.8 and mean_absolute_difference <= 3
    counterexample = "mapping_undefined" if not conjecture_holds else ""

    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")