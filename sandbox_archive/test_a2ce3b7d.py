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

def sieve_of_eratosthenes(n):
    primes = [True] * (n + 1)
    p = 2
    while p * p <= n:
        if primes[p]:
            for i in range(p * p, n + 1, p):
                primes[i] = False
        p += 1
    return [p for p in range(2, n) if primes[p]]

def legendre_symbol(a, p):
    if a == 0:
        return 0
    elif a < 0:
        return -legendre_symbol(-a, p)
    elif a % 2 == 0:
        return legendre_symbol(a // 2, p) * (-1)**((p * p - 1) // 8)
    else:
        if p % 8 in (3, 5):
            return -legendre_symbol(p, a)
        else:
            return legendre_symbol(p, a)

def fast_power(base, exp, mod):
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp >> 1
        base = (base * base) % mod
    return result

def generate_truth_table(n):
    return [random.choice([-1, 1]) for _ in range(2**n)]

def compute_p_n(n):
    primes = sieve_of_eratosthenes(2**n)
    return primes[-1]

def compute_chi_n(k, p):
    return fast_power(k, (p - 1) // 2, p)

def compute_Q(f, n):
    p_n = compute_p_n(n)
    chi_n = [compute_chi_n(k, p_n) for k in range(2**n)]
    max_sum = 0
    current_sum = 0
    for k in range(1, 2**n):
        current_sum += f[k-1] * chi_n[k-1]
        max_sum = max(max_sum, abs(current_sum))
    return (max_sum / math.sqrt(p_n))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [10, 12, 14, 16]
    results_A = []
    results_B = []
    results_C = []

    for n in n_values:
        Q_A = [compute_Q(generate_truth_table(n), n) for _ in range(30)]
        Q_B = [compute_Q(generate_truth_table(n), n) for _ in range(30)]
        Q_C = [compute_Q(generate_truth_table(n), n) for _ in range(30)]

        results_A.extend(Q_A)
        results_B.extend(Q_B)
        results_C.extend(Q_C)

    median_Q_A = sorted(results_A)[len(results_A) // 2]
    median_Q_B = sorted(results_B)[len(results_B) // 2]
    max_Q_C = max(results_C)

    conjecture_holds = median_Q_C >= 1.5 * median_Q_B and max_Q_A < n_values[0] ** (1/4)
    counterexample = "" if conjecture_holds else "median Q(C) < 1.5 * median Q(B) or max Q(A) >= n^{1/4}"

    return {
        "metric_name": "Q",
        "metric_value": max(results_C),
        "instances_tested": len(results_A) + len(results_B) + len(results_C),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or sieve_of_eratosthenes(30)[:30]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}**}}")
        results.append(result)

    median_Q_C = sorted([r["metric_value"] for r in results if "Q(C)" in r["counterexample"]])[len(results) // 2]
    max_Q_A = max(r["metric_value"] for r in results if "Q(A)" in r["counterexample"])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results) or support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results)/len(results)} std=... support_fraction={support_fraction}")
    elif any("Q(B) >= Q(C)" in r["counterexample"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "Q(B) >= Q(C)" in result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"Q(B) >= Q(C)\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} < 0.8")