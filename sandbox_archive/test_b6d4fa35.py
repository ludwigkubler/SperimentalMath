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
    
    def gaussian_elimination(A, b):
        n = len(A)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
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
        return [b[i][-1] for i in range(n)]

    def sdp_relaxation(n):
        # Simplified SDP relaxation for polynomial approximation
        A = [[0] * (n + 1) for _ in range(n + 1)]
        b = [0] * (n + 1)
        for i in range(1, n + 1):
            A[0][i] = A[i][0] = 2
            A[i][i] = -1
            b[i] = 1
        return gaussian_elimination(A, b)[0]

    def degree_of_majority(n):
        # Simplified approximation of the degree using SDP relaxation
        return sdp_relaxation(n)

    n = random.choice([5, 10, 15, 20, 30, 40])
    epsilon = 1 / n
    degree = degree_of_majority(n)
    
    if degree < math.sqrt(n):
        return {
            "metric_name": "approximation_degree",
            "metric_value": degree,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Degree {degree} is less than sqrt({n})"
        }
    
    return {
        "metric_name": "approximation_degree",
        "metric_value": degree,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["conjecture_holds"]]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):.2f} support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Degree less than sqrt(n)\" first_failing_seed={first_failing_seed}")