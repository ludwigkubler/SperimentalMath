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

def fast_walsh_hadamard_transform(a):
    n = len(a)
    if n == 1:
        return a
    even = fast_walsh_hadamard_transform(a[0::2])
    odd = fast_walsh_hadamard_transform(a[1::2])
    result = [0] * n
    for k in range(n // 2):
        result[k] = even[k] + odd[k]
        result[k + n // 2] = even[k] - odd[k]
    return result

def additivity_energy(fourier_coeffs):
    n = len(fourier_coeffs)
    energy = 0
    for i in range(n):
        for j in range(i + 1, n):
            if fourier_coeffs[i] * fourier_coeffs[j] != 0:
                energy += 1
    return energy

def sipser_function(x, n):
    result = 0
    for i in range(n):
        result ^= x[i]
    return result

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_energy = 0
    instances_tested = 0
    for n in n_values:
        for _ in range(5):  # Test each n 5 times
            x = [random.randint(0, 1) for _ in range(n)]
            fourier_coeffs = fast_walsh_hadamard_transform([sipser_function(x[:i], i) for i in range(n + 1)])
            energy = additivity_energy(fourier_coeffs)
            total_energy += energy
            instances_tested += 1
    mean_energy = total_energy / (instances_tested * len(n_values))
    conjecture_holds = mean_energy >= 2 ** (len(n_values) / 2)
    counterexample = "" if conjecture_holds else f"mean_energy={mean_energy}"
    return {
        "metric_name": "additivity_energy",
        "metric_value": mean_energy,
        "instances_tested": instances_tested,
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

    mean_energy = sum(r["metric_value"] for r in results) / len(results)
    std_energy = math.sqrt(sum((r["metric_value"] - mean_energy)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_energy} std={std_energy} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_energy} std={std_energy} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='additivity_energy<{mean_energy}>' first_failing_seed={first_failing_seed}")