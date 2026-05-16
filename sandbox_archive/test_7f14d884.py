# auto-injected by SEC sandbox
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from fractions import Fraction

def mobius(k):
    if k == 1:
        return 1
    factors = set()
    n = k
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            factors.add(i)
            while n % i == 0:
                n //= i
    if n > 1:
        factors.add(n)
    if len(factors) % 2 == 1:
        return -1
    else:
        return 0

def fast_walsh_hadamard(f):
    n = len(f)
    if n == 1:
        return f
    half = n // 2
    even = fast_walsh_hadamard(f[:half])
    odd = fast_walsh_hadamard(f[half:])
    result = [0] * n
    for i in range(half):
        result[i] = even[i] + odd[i]
        result[i + half] = even[i] - odd[i]
    return result

def generate_function(n, family, seed):
    random.seed(seed)
    if family == "balanced_uniform":
        f = [random.choice([-1, 1]) for _ in range(2**n)]
        while sum(f) != 0:
            f = [random.choice([-1, 1]) for _ in range(2**n)]
        return f
    elif family == "dictators":
        index = random.randint(0, n-1)
        f = [1] * (2**n)
        for i in range(2**n):
            if (i >> index) & 1 == 0:
                f[i] = -1
        return f
    elif family == "AND_n":
        return [1 if i == (1 << n) - 1 else -1 for i in range(2**n)]
    elif family == "OR_n":
        return [-1 if i == 0 else 1 for i in range(2**n)]
    elif family == "MAJ_n":
        return [1 if bin(i).count('1') > n // 2 else -1 for i in range(2**n)]
    elif family == "PARITY_n":
        return [1 if bin(i).count('1') % 2 == 0 else -1 for i in range(2**n)]
    elif family == "k_juntas":
        k = random.randint(1, 3)
        indices = random.sample(range(n), k)
        f = [1] * (2**n)
        for i in range(2**n):
            for j in indices:
                if (i >> j) & 1 == 0:
                    f[i] = -1
                    break
        return f
    elif family == "TRIBES":
        f = [1] * (2**n)
        for i in range(2**n):
            count = bin(i).count('1')
            if count < n // 3:
                f[i] = -1
            elif count > 2 * n // 3:
                f[i] = -1
        return f
    elif family == "addressing":
        f = [1] * (2**n)
        for i in range(2**n):
            if i % 2 == 0:
                f[i] = -1
        return f
    else:
        raise ValueError("Unknown family")

def compute_metrics(f, n):
    hat_f = fast_walsh_hadamard(f)
    hat_f_sq = [x**2 for x in hat_f]
    W_k = [0] * (n + 1)
    for S in range(2**n):
        k = bin(S).count('1')
        W_k[k] += hat_f_sq[S]
    I_f = sum(k * hat_f_sq[S] for S in range(2**n) for k in range(n + 1) if (S >> k) & 1)
    M_f = sum(mobius(k) * W_k[k] for k in range(1, n + 1))
    return W_k, I_f, M_f

def run_trial(seed):
    random.seed(seed)
    n_values = [4, 5, 6, 7, 8, 9, 10]
    families = ["balanced_uniform", "dictators", "AND_n", "OR_n", "MAJ_n", "PARITY_n", "k_juntas", "TRIBES", "addressing"]
    max_value = 0.0
    counterexample = ""
    instances_tested = 0
    conjecture_holds = True

    for n in n_values:
        for family in families:
            f = generate_function(n, family, seed)
            W_k, I_f, M_f = compute_metrics(f, n)
            value = abs(M_f) * math.sqrt(1 + I_f)
            instances_tested += 1
            if value > max_value:
                max_value = value
                if value > 2.0:
                    conjecture_holds = False
                    counterexample = f"n={n}, family={family}, seed={seed}, value={value}"

    return {
        "metric_name": "max(|M(f)|*sqrt(1+I(f)))",
        "metric_value": max_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    metric_values = []
    support_fraction = 0.0
    max_value = 0.0
    first_failing_seed = None

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        metric_values.append(result["metric_value"])
        if result["conjecture_holds"]:
            support_fraction += 1
        if result["metric_value"] > max_value:
            max_value = result["metric_value"]
            if result["metric_value"] > 2.0 and first_failing_seed is None:
                first_failing_seed = seed

    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction /= len(metric_values)

    if first_failing_seed is not None:
        print(f'RESULT: FALSIFIED counterexample="max(|M(f)|*sqrt(1+I(f)))={max_value}" first_failing_seed={first_failing_seed}')
    elif support_fraction >= 0.8:
        print(f'RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}')
    else:
        print('RESULT: INCONCLUSIVE reason=insufficient_support')