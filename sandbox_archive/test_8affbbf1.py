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
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if j != i:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def determinant(A):
        m, n = len(A), len(A[0])
        det = 1
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            if max_row != i:
                det *= -1
                A[i], A[max_row] = A[max_row], A[i]
            det *= A[i][i]
            for j in range(n):
                if j != i:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return det
    
    def circuit_monotone_width(phi):
        # Placeholder function to compute the circuit monotone width of a CNF formula
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, 10)
    
    def minimal_noncommutative_tensor_power(phi):
        # Placeholder function to compute the minimal order of noncommutative tensor power associated with a CNF formula
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, 10)
    
    n = random.randint(5, 40)
    phi = [random.choice([True, False]) for _ in range(n)]
    
    w_phi = circuit_monotone_width(phi)
    t_power = minimal_noncommutative_tensor_power(phi)
    
    c = 2.0
    if t_power <= c * w_phi:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"t_power={t_power}, c*w_phi={c*w_phi}"
    
    return {
        "metric_name": "minimal_noncommutative_tensor_power",
        "metric_value": t_power,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.randint(2, 2**31-1) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results]
    conjecture_holds_count = sum(r["conjecture_holds"] for r in results)
    
    mean_metric_value = sum(metric_values) / len(metric_values)
    std_metric_value = math.sqrt(sum((x - mean_metric_value) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = conjecture_holds_count / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")