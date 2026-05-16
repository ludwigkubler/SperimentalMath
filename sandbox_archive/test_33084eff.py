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
    count = 0
    for p in range(2, int(math.sqrt(n)) + 1):
        if n % p == 0:
            if n % (p * p) == 0:
                return 0
            count += 1
            n //= p
    if n > 1:
        count += 1
    return (-1) ** count

def fast_walsh_hadamard(f):
    n = len(f)
    if n == 1:
        return f
    half = n // 2
    even = fast_walsh_hadamard([f[i] for i in range(0, n, 2)])
    odd = fast_walsh_hadamard([f[i] for i in range(1, n, 2)])
    result = [0] * n
    for i in range(half):
        result[i] = even[i] + odd[i]
        result[i + half] = even[i] - odd[i]
    return result

def generate_function(family, n, seed):
    random.seed(seed)
    if family == 'balanced_uniform':
        return [random.choice([-1, 1]) for _ in range(2**n)]
    elif family == 'dictators':
        k = random.randint(0, n-1)
        return [random.choice([-1, 1]) if (i >> k) & 1 else random.choice([-1, 1]) for i in range(2**n)]
    elif family == 'AND_n':
        return [1 if i == 2**n - 1 else -1 for i in range(2**n)]
    elif family == 'OR_n':
        return [-1 if i == 0 else 1 for i in range(2**n)]
    elif family == 'MAJ_n':
        return [1 if bin(i).count('1') > n // 2 else -1 for i in range(2**n)]
    elif family == 'PARITY_n':
        return [1 if bin(i).count('1') % 2 == 0 else -1 for i in range(2**n)]
    elif family == 'k_juntas':
        k = random.randint(1, 3)
        relevant_bits = random.sample(range(n), k)
        return [1 if sum((i >> j) & 1 for j in relevant_bits) % 2 == 0 else -1 for i in range(2**n)]
    elif family == 'TRIBES':
        tribes = [random.sample(range(n), random.randint(1, n)) for _ in range(random.randint(2, 5))]
        return [1 if any(all((i >> j) & 1 for j in tribe) for tribe in tribes) else -1 for i in range(2**n)]
    elif family == 'addressing':
        return [1 if i == random.randint(0, 2**n - 1) else -1 for i in range(2**n)]
    else:
        raise ValueError("Unknown family")

def compute_metrics(f, n):
    hat_f = fast_walsh_hadamard(f)
    hat_f_sq = [x**2 for x in hat_f]
    W_k = defaultdict(float)
    for S in range(2**n):
        k = bin(S).count('1')
        W_k[k] += hat_f_sq[S]
    M = sum(mobius(k) * W_k[k] for k in W_k)
    I = sum(k * W_k[k] for k in W_k)
    return M, I

def run_trial(seed):
    random.seed(seed)
    n_values = [4, 5, 6, 7, 8, 9, 10]
    families = ['balanced_uniform', 'dictators', 'AND_n', 'OR_n', 'MAJ_n', 'PARITY_n', 'k_juntas', 'TRIBES', 'addressing']
    instances_tested = 0
    max_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for family in families:
            f = generate_function(family, n, seed)
            M, I = compute_metrics(f, n)
            value = abs(M) * math.sqrt(1 + I)
            instances_tested += 1
            if value > max_value:
                max_value = value
            if value > 2.0:
                conjecture_holds = False
                counterexample = f"family={family}, n={n}, M={M}, I={I}, value={value}"

    return {
        "metric_name": "max_M_sqrt_I",
        "metric_value": max_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    metric_values = []
    support_counts = 0
    total_instances = 0

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        metric_values.append(result["metric_value"])
        if result["conjecture_holds"]:
            support_counts += 1
        total_instances += result["instances_tested"]

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = support_counts / len(seeds)

    if all(result["conjecture_holds"] for result in [run_trial(seed) for seed in seeds]):
        print(f"RESULT: SUPPORTED mean={mean_metric:.4f} std={std_metric:.4f} support_fraction={support_fraction:.4f}")
    else:
        max_value = max(result["metric_value"] for result in [run_trial(seed) for seed in seeds])
        first_failing_seed = next(seed for seed in seeds if not run_trial(seed)["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in [run_trial(seed) for seed in seeds] if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")