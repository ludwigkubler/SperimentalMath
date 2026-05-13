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

def generate_xor_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def fast_walsh_hadamard_transform(f):
    n = len(f)
    while n > 1:
        half_n = n // 2
        for i in range(half_n):
            for j in range(n):
                if j < half_n:
                    f[j] += f[j + half_n]
                else:
                    f[j] -= f[j - half_n]
        n //= 2
    return [x / (1 << len(f)) for x in f]

def elementary_symmetric_polynomial_expansion(coeffs):
    n = len(coeffs)
    C = [0] * (n + 1)
    C[0] = 1
    for coeff in coeffs:
        for i in range(n, 0, -1):
            C[i] += i * C[i - 1]
        C[0] -= coeff
    return sum(C)

def parity_check(f):
    n = len(f)
    communication_complexity = 0
    for i in range(2**n):
        if f[i]:
            communication_complexity += 1
    return communication_complexity

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    f = generate_xor_function(n)
    transformed_f = fast_walsh_hadamard_transform(f)
    C = elementary_symmetric_polynomial_expansion(transformed_f)
    D = parity_check(f)
    return {
        "metric_name": "Communication Complexity",
        "metric_value": D,
        "instances_tested": 1,
        "conjecture_holds": D >= math.log(C, 2),
        "counterexample": "" if D >= math.log(C, 2) else f"Counterexample for n={n}, C(f)={C}, D(f)={D}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        counterexample = next(res["counterexample"] for res in results if res["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")