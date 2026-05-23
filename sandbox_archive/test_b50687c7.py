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
            # Find pivot
            max_row = i
            for k in range(i+1, n):
                if abs(A[k][i]) > abs(A[max_row][i]):
                    max_row = k
            A[i], A[max_row] = A[max_row], A[i]
            
            # Eliminate below
            pivot = A[i][i]
            for k in range(i+1, n):
                factor = A[k][i] / pivot
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
        
        # Back substitution
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = A[i][-1] / A[i][i]
            for k in range(i-1, -1, -1):
                A[k][-1] -= A[k][i] * x[i]
        
        return x

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
        sign = 1
        for i in range(n):
            submatrix = [row[:i] + row[i+1:] for row in A[1:]]
            det += sign * A[0][i] * determinant(submatrix)
            sign *= -1
        return det

    def is_invertible(A):
        return determinant(A) != 0

    n = random.randint(5, 40)
    circuit_depth = random.randint(n // 2, n)

    # Construct a quandle group representation (simplified example)
    quandle_group = [[i * j % n for j in range(n)] for i in range(n)]

    # Compute the minimal order of non-trivial elements
    min_order = float('inf')
    for i in range(1, n):
        if is_invertible(quandle_group[i]):
            order = 1
            current = quandle_group[i]
            while current != [j * i % n for j in range(n)]:
                current = matrix_multiplication(current, quandle_group[i])
                order += 1
            min_order = min(min_order, order)

    return {
        "metric_name": "Minimal Order of Quandle Group",
        "metric_value": min_order,
        "instances_tested": 1,
        "conjecture_holds": False if min_order > n**2 else True,
        "counterexample": "mapping_undefined" if min_order > n**2 else ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [random.randint(1000, 9999) for _ in range(30)]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")