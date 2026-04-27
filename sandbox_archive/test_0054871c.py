# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def binomial(n, k):
    if k > n:
        return 0
    result = 1
    for i in range(k):
        result *= (n - i)
        result //= (i + 1)
    return result

def hamming_weight(x):
    return bin(x).count('1')

def A_w(f, w):
    n = len(f)
    return sum(f(x) * (-1)**hamming_weight(x) for x in range(2**n) if hamming_weight(x) == w) / binomial(n, w)

def sigma(f):
    n = len(f)
    return sum(A_w(f, w) * math.log2(binomial(n, w)) for w in range(n + 1))

def Var(f):
    n = len(f)
    mean = sum(hamming_weight(x) * f(x) for x in range(2**n)) / (2**n)
    return sum((hamming_weight(x) - mean)**2 * f(x) for x in range(2**n))

def S_2(f):
    n = len(f)
    max_size = 8
    min_size = float('inf')
    for s in range(1, max_size + 1):
        for circuit in generate_circuits(n, s):
            if evaluate_circuit(circuit, f) == f:
                min_size = min(min_size, s)
                break
        if min_size < float('inf'):
            break
    return min_size

def generate_circuits(n, size):
    # Placeholder for circuit generation logic
    # This is a simplified version and may not cover all possible circuits
    if size == 0:
        yield {}
    else:
        for i in range(1 << n):
            for j in range(i + 1, 1 << (n + 1)):
                yield {i: j}

def evaluate_circuit(circuit, f):
    # Placeholder for circuit evaluation logic
    # This is a simplified version and may not cover all possible circuits
    return f

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [3, 4, 5] + list(range(6, 13))
    total_instances = 0
    support_count = 0
    max_violation_ratio = 0
    counterexample = ""

    for n in n_values:
        if n <= 20:
            instances = [random.randint(0, 1) for _ in range(2**n)] * (2000 if n >= 6 else 1)
        else:
            instances = [random.randint(0, 1) for _ in range(2**n)]

        for f in instances:
            A_w_values = [A_w(f, w) for w in range(n + 1)]
            sigma_f = sigma(f)
            Var_value = Var(f)
            S_2_value = S_2(f)

            if sigma_f == 0 or S_2_value == 0:
                continue

            r_f = Var_value / ((n + 1) * abs(sigma_f) * math.log2(1 + S_2_value))
            total_instances += 1
            support_count += int(r_f <= 1)

            if r_f > max_violation_ratio:
                max_violation_ratio = r_f

    conjecture_holds = support_count / total_instances >= 0.99 and max_violation_ratio <= 1.0
    return {
        "metric_name": "max_violation_ratio",
        "metric_value": max_violation_ratio,
        "instances_tested": total_instances,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample if not conjecture_holds else ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")