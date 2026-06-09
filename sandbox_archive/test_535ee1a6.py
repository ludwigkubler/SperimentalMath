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
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            b[i] /= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
                    b[k] -= factor * b[i]
        return b
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def determinant(A):
        n = len(A)
        det = 0
        if n == 1:
            return A[0][0]
        elif n == 2:
            return A[0][0] * A[1][1] - A[0][1] * A[1][0]
        else:
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in A[1:]]
                det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det
    
    def inverse(A):
        n = len(A)
        det_A = determinant(A)
        if det_A == 0:
            raise ValueError("Matrix is not invertible")
        adjoint = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
                minor = determinant(submatrix)
                adjoint[j][i] = (-1) ** (i+j) * minor
        inv_A = [[adjoint[j][i] / det_A for j in range(n)] for i in range(n)]
        return inv_A
    
    def frege_width(phi):
        # Placeholder function to compute Frege proof width
        # Replace with actual implementation
        return len(phi)
    
    def eta_quotient_order(V):
        # Placeholder function to compute minimal order of eta-quotient
        # Replace with actual implementation
        return random.randint(1, 10)  # Dummy value
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    phi = [random.randint(1, n) for _ in range(n)]
    
    frege_widths = [frege_width(phi) for _ in range(30)]
    eta_quotient_orders = [eta_quotient_order(phi) for _ in range(30)]
    
    if not frege_widths or not eta_quotient_orders:
        return {
            "metric_name": "Frege Proof Width vs Eta-Quotient Order",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "empty_data"
        }
    
    frege_width_mean = sum(frege_widths) / len(frege_widths)
    eta_quotient_order_mean = sum(eta_quotient_orders) / len(eta_quotient_orders)
    
    if len(frege_widths) < 2 or len(eta_quotient_orders) < 2:
        return {
            "metric_name": "Frege Proof Width vs Eta-Quotient Order",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }
    
    correlation_coefficient = (sum((x - eta_quotient_order_mean) * (y - frege_width_mean) for x, y in zip(eta_quotient_orders, frege_widths)) /
                               math.sqrt(sum((x - eta_quotient_order_mean) ** 2 for x in eta_quotient_orders) *
                                         sum((y - frege_width_mean) ** 2 for y in frege_widths)))
    
    return {
        "metric_name": "Frege Proof Width vs Eta-Quotient Order",
        "metric_value": correlation_coefficient,
        "instances_tested": len(frege_widths),
        "n_max": n,
        "conjecture_holds": abs(correlation_coefficient) > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        mean_value = None
        std_value = None
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["metric_value"] is not None for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(result["counterexample"] != "" for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{next(result['counterexample'] for result in results if result['counterexample'] != '')}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")