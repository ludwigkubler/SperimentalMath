# auto-injected by SEC sandbox
import json
import os
import time
import re
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from collections import defaultdict

def mobius(n):
    if n == 1:
        return 1
    factors = set()
    temp = n
    for i in range(2, int(math.sqrt(temp)) + 1):
        if temp % i == 0:
            factors.add(i)
            while temp % i == 0:
                temp //= i
    if temp > 1:
        factors.add(temp)
    if len(factors) % 2 == 1:
        return -1
    else:
        return 0

def fast_walsh_hadamard(f):
    n = len(f)
    if n == 1:
        return f
    half = n // 2
    even = fast_walsh_hadamard(f[:half] + f[half:])
    odd = fast_walsh_hadamard(f[half:] + f[:half])
    return [e + o for e, o in zip(even, odd)] + [e - o for e, o in zip(even, odd)]

def generate_function(n, family, seed):
    random.seed(seed)
    if family == "balanced_uniform":
        f = [random.choice([-1, 1]) for _ in range(2**n)]
        while sum(f) != 0:
            f = [random.choice([-1, 1]) for _ in range(2**n)]
        return f
    elif family == "dictators":
        index = random.randint(0, n-1)
        f = [-1] * (2**n)
        for i in range(2**n):
            if (i >> index) & 1:
                f[i] = 1
        return f
    elif family == "AND_n":
        return [1 if all((i >> j) & 1 for j in range(n)) else -1 for i in range(2**n)]
    elif family == "OR_n":
        return [1 if any((i >> j) & 1 for j in range(n)) else -1 for i in range(2**n)]
    elif family == "MAJ_n":
        return [1 if sum((i >> j) & 1 for j in range(n)) > n//2 else -1 for i in range(2**n)]
    elif family == "PARITY_n":
        return [1 if bin(i).count('1') % 2 == 0 else -1 for i in range(2**n)]
    elif family == "k_juntas":
        k = random.randint(1, 3)
        indices = random.sample(range(n), k)
        f = [-1] * (2**n)
        for i in range(2**n):
            if sum((i >> j) & 1 for j in indices) > k//2:
                f[i] = 1
        return f
    elif family == "TRIBES":
        tribes = [random.sample(range(n), n//3) for _ in range(3)]
        f = [-1] * (2**n)
        for i in range(2**n):
            counts = [sum((i >> j) & 1 for j in tribe) for tribe in tribes]
            if max(counts) > n//6:
                f[i] = 1
        return f
    elif family == "addressing":
        index = random.randint(0, n-1)
        f = [-1] * (2**n)
        for i in range(2**n):
            if (i >> index) & 1:
                f[i] = 1
        return f

def compute_metrics(f, n):
    fourier = fast_walsh_hadamard(f)
    fourier_sq = [x**2 for x in fourier]
    W_k = defaultdict(float)
    I = 0.0
    for S in range(2**n):
        k = bin(S).count('1')
        W_k[k] += fourier_sq[S]
        I += k * fourier_sq[S]
    M = 0.0
    for k in range(1, n+1):
        M += mobius(k) * W_k[k]
    return M, I, W_k

def run_trial(seed):
    random.seed(seed)
    n_values = [4, 5, 6, 7, 8, 9, 10]
    families = ["balanced_uniform", "dictators", "AND_n", "OR_n", "MAJ_n", "PARITY_n", "k_juntas", "TRIBES", "addressing"]
    max_metric = 0.0
    counterexample = ""
    instances_tested = 0
    conjecture_holds = True

    for n in n_values:
        for family in families:
            f = generate_function(n, family, seed)
            M, I, W_k = compute_metrics(f, n)
            metric = abs(M) * math.sqrt(1 + I)
            instances_tested += 1
            if metric > max_metric:
                max_metric = metric
            if metric > 2.0:
                conjecture_holds = False
                counterexample = f"n={n}, family={family}, M={M}, I={I}, metric={metric}"

    return {
        "metric_name": "max(|M(f)|*sqrt(1+I(f)))",
        "metric_value": max_metric,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    metric_values = []
    support_fraction = 0.0
    first_failing_seed = None
    counterexample = ""

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        metric_values.append(result["metric_value"])
        if result["conjecture_holds"]:
            support_fraction += 1
        else:
            if first_failing_seed is None:
                first_failing_seed = seed
                counterexample = result["counterexample"]

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction /= len(seeds)

    if all(result["conjecture_holds"] for result in [run_trial(seed) for seed in seeds]):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in [run_trial(seed) for seed in seeds]):
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")