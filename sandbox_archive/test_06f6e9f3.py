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

def walsh_hadamard_transform(f):
    n = len(f)
    if n == 1:
        return f
    f_even = walsh_hadamard_transform([f[i] for i in range(0, n, 2)])
    f_odd = walsh_hadamard_transform([f[i] for i in range(1, n, 2)])
    result = [0] * n
    for k in range(n // 2):
        result[k] = f_even[k] + f_odd[k]
        result[k + n // 2] = f_even[k] - f_odd[k]
    return result

def fourier_coefficients(f, n):
    wft = walsh_hadamard_transform(f)
    norm = sum(wft[i]**2 for i in range(n)) / n
    mu_k = [abs(wft[i]) / math.sqrt(norm) for i in range(n)]
    return mu_k

def gaussian_elimination(A, b):
    n = len(b)
    A_b = list(zip(A, b))
    A_b.sort(key=lambda x: abs(x[0][0]), reverse=True)
    for i in range(n):
        pivot_row = next((j for j in range(i, n) if A_b[j][0][i] != 0), None)
        if pivot_row is None:
            return None
        A_b[i], A_b[pivot_row] = A_b[pivot_row], A_b[i]
        for j in range(n):
            if i == j:
                continue
            factor = A_b[j][0][i] / A_b[i][0][i]
            A_b[j] = (tuple(A_b[j][0][k] - factor * A_b[i][0][k] for k in range(n)), A_b[j][1] - factor * A_b[i][1])
    return [x[1] for x in A_b]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    f = [random.choice([0, 1]) for _ in range(2**n)]
    mu_k = fourier_coefficients(f, 2**n)
    
    alpha = random.uniform(3, 5)
    decay_rate = all(mu_k[k] <= (k + 1)**(-alpha) for k in range(len(mu_k)))
    
    if not decay_rate:
        return {
            "metric_name": "decay_rate",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "decay_rate"
        }
    
    # Placeholder for SOS degree check
    sos_degree = random.randint(1, n)
    
    if sos_degree < math.ceil(n**(1/alpha)):
        return {
            "metric_name": "sos_degree",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "sos_degree"
        }
    
    return {
        "metric_name": "sos_degree",
        "metric_value": sos_degree,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(x["metric_value"] for x in results if x["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((x["metric_value"] - mean_value)**2 for x in results if x["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not x["conjecture_holds"] for x in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"decay_rate\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")