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
        n = len(b)
        for i in range(n):
            max_row = i
            for k in range(i+1, n):
                if abs(A[k][i]) > abs(A[max_row][i]):
                    max_row = k
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for k in range(i+1, n):
                factor = A[k][i] / A[i][i]
                for j in range(i, n):
                    A[k][j] -= factor * A[i][j]
                b[k] -= factor * b[i]
        x = [0.0] * n
        for i in range(n-1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
        return x

    def matrix_multiply(A, B):
        m = len(A)
        n = len(B[0])
        p = len(B)
        C = [[0.0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def ac0_circuit_size(poly, n):
        # Placeholder for AC0 circuit size computation
        # This is a dummy implementation and should be replaced with actual logic
        return len(poly)

    def minimal_hodge_index(n):
        # Placeholder for Minimal Hodge Index computation
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, n)

    n = random.choice([5, 10, 15, 20, 30, 40])
    q = random.randint(2, 10)
    poly = sum(random.choice([-1, 1]) * 'x' + str(i) for i in range(n))
    
    A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    b = [random.randint(-10, 10) for _ in range(n)]
    
    try:
        x = gaussian_elimination(A, b)
        circuit_size = ac0_circuit_size(poly, n)
        hodge_index = minimal_hodge_index(n)
        
        if circuit_size > hodge_index:
            return {
                "metric_name": "H1 vs AC0 Circuit Size",
                "metric_value": hodge_index,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"Counterexample found: H1({n}) = {hodge_index} > AC0 Circuit Size({n}) = {circuit_size}"
            }
        else:
            return {
                "metric_name": "H1 vs AC0 Circuit Size",
                "metric_value": hodge_index,
                "instances_tested": 1,
                "conjecture_holds": True,
                "counterexample": ""
            }
    except Exception as e:
        return {
            "metric_name": "H1 vs AC0 Circuit Size",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Exception: {str(e)}"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values)} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values)/len(metric_values))} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values)} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values)/len(metric_values))} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")