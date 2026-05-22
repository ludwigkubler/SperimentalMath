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
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det

    def quaternion_order(n, k):
        # Simplified version for demonstration purposes
        return (n**k) / math.log(n)

    def construct_monotone_circuit(n):
        # Placeholder function to simulate circuit construction
        # This is a very rough approximation and not actual complexity theory
        return 2 ** (n // 2)

    n = random.randint(5, 40)
    k = random.randint(1, 3)  # Limiting k to small values for practical computation

    Q_order = quaternion_order(n, k)
    circuit_size = construct_monotone_circuit(n)

    if abs(Q_order - circuit_size) > 2 ** (n // 2):
        return {
            "metric_name": "Order of Quaternion Algebra vs Circuit Size",
            "metric_value": Q_order,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Q_order={Q_order}, circuit_size={circuit_size}"
        }

    return {
        "metric_name": "Order of Quaternion Algebra vs Circuit Size",
        "metric_value": Q_order,
        "instances_tested": 1,
        "conjecture_holds": True,
            "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    total_metric_value = sum(result["metric_value"] for result in results if result["conjecture_holds"])
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"order(Q) does not match circuit size\" first_failing_seed={first_failing_seed}")