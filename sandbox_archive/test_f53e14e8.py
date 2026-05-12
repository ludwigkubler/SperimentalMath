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

def fast_walsh_hadamard_transform(f):
    n = len(f)
    if n == 1:
        return f
    even = fast_walsh_hadamard_transform([f[i] for i in range(0, n, 2)])
    odd = fast_walsh_hadamard_transform([f[i] for i in range(1, n, 2)])
    result = [0] * n
    for k in range(n // 2):
        result[k] = even[k] + odd[k]
        result[k + n // 2] = even[k] - odd[k]
    return result

def generate_random_boolean_function(n):
    return [random.randint(0, 1) for _ in range(2**n)]

def compute_fourier_coefficients(f):
    n = int(math.log2(len(f)))
    f_transformed = fast_walsh_hadamard_transform(f)
    fourier_coeffs = [abs(f_transformed[k] / len(f)) for k in range(n)]
    return sum(fourier_coeffs)

def is_in_acc0_circuit_size(f):
    # Placeholder function to check if a boolean function can be computed by an ACC⁰ circuit
    # This is a dummy implementation and should be replaced with actual logic
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10
    f = generate_random_boolean_function(n)
    fourier_sum = compute_fourier_coefficients(f)
    conjecture_holds = fourier_sum < 2**(n/2) * math.sqrt(n)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "Fourier Coefficient Sum",
        "metric_value": fourier_sum,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")