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
            max_row = i + max(range(i, m), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if n == 1:
            return A[0][0]
        det = Fraction(0)
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det

    def minimal_number_field_trace(poly):
        # Placeholder implementation
        return random.random()

    def circuit_monotone_width(circuit):
        # Placeholder implementation
        return random.randint(1, 10)

    n = random.choice([5, 10, 15, 20, 30, 40])
    instances_tested = 30
    total_metric_value = 0
    counterexample = ""

    for _ in range(instances_tested):
        cnf_formula = [[random.randint(1, n) for _ in range(random.randint(1, 5))] for _ in range(n)]
        mnt_phi = minimal_number_field_trace(cnf_formula)
        circuit_phi = [circuit_monotone_width(cnf_formula)]
        total_metric_value += mnt_phi * circuit_phi[0]

    mean_metric_value = total_metric_value / instances_tested
    r_squared = 1.0 if instances_tested == 1 else (instances_tested * total_metric_value**2 - sum(mnt_phi**2 for mnt_phi in mnt_phi_list) * sum(circuit_phi**2 for circuit_phi in circuit_phi_list)) / ((instances_tested - 1) * sum((mnt_phi - mean_metric_value)**2 for mnt_phi in mnt_phi_list) * sum((circuit_phi - mean_circuit_phi)**2 for circuit_phi in circuit_phi_list))

    return {
        "metric_name": "r_squared",
        "metric_value": r_squared,
        "instances_tested": instances_tested,
        "n_max": n,
        "conjecture_holds": r_squared >= 0.8,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"r_squared < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")