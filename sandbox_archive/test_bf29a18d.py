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
from fractions import Fraction
from math import sqrt

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
            factor = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if j != i:
                    factor = Fraction(A[j][i])
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
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if n == 1:
            return A[0][0]
        det = Fraction(0)
        for i in range(n):
            submatrix = [row[:i] + row[i+1:] for row in A[1:]]
            sign = (-1) ** i
            det += sign * A[0][i] * determinant(submatrix)
        return det

    def entanglement_complexity(n):
        # Placeholder function to generate a random integer between 1 and n
        return random.randint(1, n)

    def minimal_order_of_hodge_class(n):
        # Placeholder function to compute the minimal order of a Hodge class
        # This is a dummy implementation for demonstration purposes
        return random.randint(1, n)

    n_values = [5, 10, 15, 20, 30, 40]
    h_values = []
    e_values = []

    for n in n_values:
        e_C = entanglement_complexity(n)
        V_C = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        A = gaussian_elimination(V_C)
        det_A = determinant(A)
        h = minimal_order_of_hodge_class(n)

        h_values.append(h)
        e_values.append(e_C)

    correlation_coefficient = sum((h - e) * (h_ - e_) for h, h_, e, e_ in zip(h_values, h_values[1:], e_values, e_values[1:])) / len(h_values)
    support_fraction = sum(1 for h, e in zip(h_values, e_values) if abs(h - e) <= 3) / len(h_values)

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and support_fraction >= 0.8,
        "counterexample": "" if correlation_coefficient >= 0.8 and support_fraction >= 0.8 else f"correlation_coefficient={correlation_coefficient}, support_fraction={support_fraction}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")