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

def fast_walsh_hadamard(f):
    n = int(math.log2(len(f)))
    for s in range(n):
        for i in range(0, 1 << n, 1 << (s + 1)):
            for j in range(i, i + (1 << s)):
                a = f[j]
                b = f[j + (1 << s)]
                f[j] = a + b
                f[j + (1 << s)] = a - b
    return f

def mobius(k):
    if k == 1:
        return 1
    factors = set()
    n = k
    i = 2
    while i * i <= n:
        if n % i == 0:
            if i in factors:
                return 0
            factors.add(i)
            n //= i
        else:
            i += 1
    if n > 1:
        if n in factors:
            return 0
        factors.add(n)
    return (-1) ** len(factors)

def generate_function(family, n, seed):
    random.seed(seed)
    if family == 'uniform':
        return [random.choice([-1, 1]) for _ in range(1 << n)]
    elif family == 'dictators':
        k = random.randint(0, n - 1)
        return [(-1) ** ((x >> k) & 1) for x in range(1 << n)]
    elif family == 'AND':
        return [(-1) ** (x == (1 << n) - 1) for x in range(1 << n)]
    elif family == 'OR':
        return [(-1) ** (x != 0) for x in range(1 << n)]
    elif family == 'MAJ':
        return [(-1) ** (bin(x).count('1') > n // 2) for x in range(1 << n)]
    elif family == 'PARITY':
        return [(-1) ** (bin(x).count('1') % 2) for x in range(1 << n)]
    elif family == 'k-junta':
        k = random.randint(1, 3)
        vars = random.sample(range(n), k)
        return [(-1) ** sum((x >> var) & 1 for var in vars) for x in range(1 << n)]
    elif family == 'TRIBES':
        tribes = [random.sample(range(n), random.randint(1, n)) for _ in range(random.randint(2, 4))]
        return [(-1) ** sum(any((x >> var) & 1 for var in tribe) for tribe in tribes) for x in range(1 << n)]
    elif family == 'addressing':
        return [(-1) ** (x == random.randint(0, (1 << n) - 1)) for x in range(1 << n)]
    else:
        raise ValueError("Unknown family")

def run_trial(seed):
    random.seed(seed)
    families = ['uniform', 'dictators', 'AND', 'OR', 'MAJ', 'PARITY', 'k-junta', 'TRIBES', 'addressing']
    n_values = [4, 5, 6, 7, 8, 9, 10]
    max_value = 0.0
    counterexample = ""
    instances_tested = 0

    for n in n_values:
        for family in families:
            f = generate_function(family, n, seed)
            f_hat = fast_walsh_hadamard(f.copy())
            f_hat = [x / (1 << n) for x in f_hat]

            W_k = defaultdict(float)
            I = 0.0
            for S in range(1 << n):
                k = bin(S).count('1')
                W_k[k] += f_hat[S] ** 2
                I += k * f_hat[S] ** 2

            M = 0.0
            for k in W_k:
                M += mobius(k) * W_k[k]

            value = abs(M) * math.sqrt(1 + I)
            instances_tested += 1

            if value > max_value:
                max_value = value
                if value > 2.0:
                    counterexample = f"family={family}, n={n}, M={M}, I={I}, value={value}"

    conjecture_holds = max_value <= 2.0
    return {
        "metric_name": "max_M_sqrt_1_plus_I",
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
    max_value = 0.0
    first_failing_seed = None
    counterexample = ""

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        metric_values.append(result["metric_value"])
        total_instances += result["instances_tested"]
        if result["conjecture_holds"]:
            support_counts += 1
        if result["metric_value"] > max_value:
            max_value = result["metric_value"]
            if result["metric_value"] > 2.0 and first_failing_seed is None:
                first_failing_seed = seed
                counterexample = result["counterexample"]

    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = support_counts / len(seeds)

    if first_failing_seed is not None:
        print(f'RESULT: FALSIFIED counterexample="{counterexample}" first_failing_seed={first_failing_seed}')
    elif support_fraction >= 0.8:
        print(f'RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}')
    else:
        print('RESULT: INCONCLUSIVE reason=insufficient_support')