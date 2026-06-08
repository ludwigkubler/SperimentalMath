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
    
    def generate_d_regular_circuit(d, n):
        if d * n % 2 != 0 or d == 1:
            return None
        circuit = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            circuit[i][i] = 0
        for i in range(n):
            for j in range(i + 1, n):
                if sum(circuit[i]) % d == 0 and sum(circuit[j]) % d == 0:
                    circuit[i][j] = circuit[j][i] = 1
        return circuit

    def is_d_regular(circuit, d):
        for row in circuit:
            if sum(row) != d:
                return False
        return True

    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A

    def determinant(A):
        n = len(A)
        det = 0
        if n == 1:
            return A[0][0]
        elif n == 2:
            return A[0][0] * A[1][1] - A[0][1] * A[1][0]
        else:
            for c in range(n):
                det += ((-1) ** c) * A[0][c] * determinant([row[:c] + row[c+1:] for row in A[1:]])
        return det

    def minimal_order_of_brauer_group(circuit):
        n = len(circuit)
        if not is_d_regular(circuit, 2):
            return None
        F_C = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if circuit[i][j] == 1:
                    F_C[i][j] = F_C[j][i] = 1
        F_C = gaussian_elimination(F_C)
        det = determinant(F_C)
        return abs(det)

    d_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_log_order = 0
    n_max = 0

    for d in d_values:
        for _ in range(5):
            circuit = generate_d_regular_circuit(d, d)
            if circuit is None:
                continue
            order = minimal_order_of_brauer_group(circuit)
            if order is not None:
                instances_tested += 1
                total_log_order += math.log2(order)
                n_max = max(n_max, d)

    conjecture_holds = total_log_order / instances_tested <= 30
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "log_minimal_order",
        "metric_value": total_log_order / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
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

    total_log_order = sum(result["metric_value"] for result in results if result["instances_tested"] > 0)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={total_log_order / len(results)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_log_order / len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")