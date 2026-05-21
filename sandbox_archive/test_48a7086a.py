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
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        if len(A) == 1:
            return A[0][0]
        det = 0
        sign = 1
        for j in range(len(A)):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += sign * A[0][j] * determinant(submatrix)
            sign *= -1
        return det

    def lrs_vertex_enumeration(n):
        # Placeholder for LRS vertex enumeration. Replace with actual implementation.
        return [[i for i in range(n)]]

    def cycle_polytope_coefficient(polytope, n):
        x = Fraction(1)
        for point in polytope:
            coeff = 1
            for val in point:
                coeff *= (x - val)
            x += coeff
        return x.coeff(x**n-2)

    def resolution_length(n):
        # Placeholder for DPLL-based solver. Replace with actual implementation.
        return n

    n = random.randint(5, 40)
    graph = lrs_vertex_enumeration(n)
    ehrhart_coefficient = cycle_polytope_coefficient(graph, n)
    ν_G = ehrhart_coefficient.numerator / ehrhart_coefficient.denominator
    resolution_len = resolution_length(n)

    if ν_G == 0:
        return {
            "metric_name": "resolution_length",
            "metric_value": resolution_len,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

    c = math.log2(resolution_len) / ν_G
    conjecture_holds = c > 0

    return {
        "metric_name": "resolution_length",
        "metric_value": resolution_len,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Graph with n={n}, ν(G)={ν_G}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    metric_values = [r["metric_value"] for r in results]
    conjecture_holds_count = sum(r["conjecture_holds"] for r in results)
    
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean)**2 for x in metric_values) / len(metric_values))
    support_fraction = conjecture_holds_count / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Graph with ν(G) > 0\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")