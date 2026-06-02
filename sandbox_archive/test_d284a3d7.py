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
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(i, n + 1):
                A[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(i, n + 1):
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

    def frege_proof_length(phi):
        # Placeholder function to simulate Frege proof length
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(10, 50)

    def generate_quasi_platonic_solid():
        # Placeholder function to generate a quasi-platonic solid
        # This is a dummy implementation and should be replaced with actual logic
        n = random.randint(3, 6)
        phi = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        return phi

    def symmetry_group_order(phi):
        # Placeholder function to compute the order of the symmetry group
        # This is a dummy implementation and should be replaced with actual logic
        A = gaussian_elimination(phi)
        order = 1
        for row in A:
            if any(row[i] != 0 for i in range(len(row))):
                order *= len([i for i in range(len(row)) if row[i] != 0])
        return order

    phi = generate_quasi_platonic_solid()
    ord_phi = symmetry_group_order(phi)
    frege_len = frege_proof_length(phi)

    return {
        "metric_name": "Symmetry Group Order vs Frege Proof Length",
        "metric_value": abs(ord_phi - frege_len),
        "instances_tested": 1,
        "n_max": len(phi),
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_count = sum(1 for r in results if r["conjecture_holds"])
    
    if support_count >= 0.8 * len(seeds):
        RESULT = f"SUPPORTED mean={mean_value} std=NA support_fraction={support_count/len(seeds)}"
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        RESULT = f"FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}"

    print(RESULT)