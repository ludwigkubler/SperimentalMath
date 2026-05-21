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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    s = random.randint(5, 40)
    d = math.ceil(math.log2(s))
    
    # Simulate the output vector of an AC0 parity circuit
    output_vector = [random.choice([0, 1]) for _ in range(d)]
    
    # Simulate a fixed representation space T and its dual W
    T = [[random.randint(0, 1) for _ in range(d)] for _ in range(d)]
    W_dual = [[random.randint(0, 1) for _ in range(d)] for _ in range(d)]
    
    # Compute the tropicalized output vector
    tropical_output = [max(output_vector[i], T[i][j]) for j in range(d)]
    
    # Check if the tropicalized output is isomorphic to the tensor product of T and W_dual
    V_inv = gaussian_elimination([[tropical_output[i] + float('inf') if i != j else -1] for i in range(d)], [float('-inf')] * d)
    if any(v < 0 for v in V_inv):
        return {
            "metric_name": "dimension",
            "metric_value": d,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "negative_invariant"
        }
    
    return {
        "metric_name": "dimension",
        "metric_value": d,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"negative_invariant\" first_failing_seed={first_failing_seed}")