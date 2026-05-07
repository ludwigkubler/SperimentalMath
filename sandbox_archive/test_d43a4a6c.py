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

def generate_ac0_circuit(n, d):
    if n == 1:
        return [random.choice([0, 1])]
    else:
        subcircuits = [generate_ac0_circuit(n // 2, d - 1) for _ in range(2)]
        return [random.choice([0, 1]) + sum(subcircuit) % 2 for subcircuit in zip(*subcircuits)]

def fourier_transform(poly):
    n = len(poly)
    if n == 1:
        return poly
    else:
        even = fourier_transform(poly[::2])
        odd = fourier_transform(poly[1::2])
        result = [0] * n
        for k in range(n // 2):
            t = math.exp(-2j * math.pi * k / n) * odd[k]
            result[k] = even[k] + t
            result[k + n // 2] = even[k] - t
        return result

def real_stable_polynomial(circuit, n):
    if len(circuit) == 1:
        return [circuit[0]]
    else:
        subpolynomials = [real_stable_polynomial(subcircuit, n // 2) for subcircuit in zip(*circuit)]
        result = [0] * (n + 1)
        for k in range(n + 1):
            for i in range(k + 1):
                result[k] += subpolynomials[0][i] * subpolynomials[1][k - i]
        return result

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    d = random.choice([3, 4])
    circuit = generate_ac0_circuit(n, d)
    poly = real_stable_polynomial(circuit, n)
    coeff_sum = sum(abs(coeff) for coeff in poly)
    threshold = 2 ** (n ** (1 / d) / 10)
    conjecture_holds = coeff_sum >= threshold
    counterexample = "" if conjecture_holds else f"coeff_sum={coeff_sum}, threshold={threshold}"
    return {
        "metric_name": "coefficient_sum",
        "metric_value": coeff_sum,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_coeff_sum = sum(res["metric_value"] for res in results) / len(results)
    std_coeff_sum = math.sqrt(sum((res["metric_value"] - mean_coeff_sum) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_coeff_sum} std={std_coeff_sum} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")