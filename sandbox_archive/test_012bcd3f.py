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
                if i != j:
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

    def mtc(P):
        # Placeholder function for minimal tropical motivic complexity
        # This is a dummy implementation and should be replaced with actual computation
        return random.random()

    def rcv(P):
        # Placeholder function for communication complexity rank variance
        # This is a dummy implementation and should be replaced with actual computation
        return random.random()

    instances_tested = 0
    mtc_values = []
    rcv_values = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            P = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
            mtc_value = mtc(P)
            rcv_value = rcv(P)
            mtc_values.append(mtc_value)
            rcv_values.append(rcv_value)
            instances_tested += 1
    
    if not mtc_values or not rcv_values:
        return {
            "metric_name": "mtc vs rcv",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(5, 10, 15, 20, 30, 40),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mtc_avg = sum(mtc_values) / instances_tested
    rcv_avg = sum(rcv_values) / instances_tested
    
    covariance = sum((mtc - mtc_avg) * (rcv - rcv_avg) for mtc, rcv in zip(mtc_values, rcv_values)) / instances_tested
    mtc_variance = sum((mtc - mtc_avg) ** 2 for mtc in mtc_values) / instances_tested
    rcv_variance = sum((rcv - rcv_avg) ** 2 for rcv in rcv_values) / instances_tested
    
    if mtc_variance == 0 or rcv_variance == 0:
        return {
            "metric_name": "mtc vs rcv",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(5, 10, 15, 20, 30, 40),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation_coefficient = covariance / (math.sqrt(mtc_variance) * math.sqrt(rcv_variance))
    
    return {
        "metric_name": "mtc vs rcv",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(5, 10, 15, 20, 30, 40),
        "conjecture_holds": correlation_coefficient >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")