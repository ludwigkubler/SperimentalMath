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

def sieve_of_eratosthenes(limit):
    primes = [True] * (limit + 1)
    p = 2
    while (p * p <= limit):
        if (primes[p] == True):
            for i in range(p * p, limit + 1, p):
                primes[i] = False
        p += 1
    prime_numbers = []
    for p in range(2, limit):
        if primes[p]:
            prime_numbers.append(p)
    return prime_numbers

def legendre_symbol(a, p):
    if a == 0:
        return 0
    elif a < 0:
        return -legendre_symbol(-a, p)
    elif a % 2 == 0:
        return legendre_symbol(2, p) * legendre_symbol(a // 2, p)
    else:
        if (p % 8 == 1 or p % 8 == 7):
            return pow(a, (p - 1) // 2, p)
        elif (p % 8 == 3 or p % 8 == 5):
            return -pow(a, (p - 1) // 2, p)

def fast_power(base, exp, mod):
    result = 1
    base = base % mod
    while exp > 0:
        if (exp % 2) == 1:  # If exp is odd, multiply base with result
            result = (result * base) % mod
        exp = exp >> 1  # Divide the exponent by 2
        base = (base * base) % mod  # Square the base
    return result

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [10, 12, 14, 16]
    results = []

    for n in n_values:
        p_n = sieve_of_eratosthenes(2**n)[-1]
        chi_n = [legendre_symbol(k, p_n) for k in range(2**n)]
        T_f_A = [random.choice([-1, 1]) for _ in range(2**n)]
        T_f_B = [random.choice([-1, 1]) for _ in range(2**n)]
        T_f_C = [random.choice([-1, 1]) for _ in range(2**n)]

        def Q(f):
            max_sum = 0
            current_sum = 0
            for k in range(1, 2**n):
                current_sum += f[k] * chi_n[k]
                if abs(current_sum) > max_sum:
                    max_sum = abs(current_sum)
            return max_sum / math.sqrt(p_n)

        Q_A = Q(T_f_A)
        Q_B = Q(T_f_B)
        Q_C = Q(T_f_C)

        results.append({
            "n": n,
            "Q_A": Q_A,
            "Q_B": Q_B,
            "Q_C": Q_C
        })

    median_Q_A = sorted([r["Q_A"] for r in results])[len(results) // 2]
    median_Q_B = sorted([r["Q_B"] for r in results])[len(results) // 2]
    median_Q_C = sorted([r["Q_C"] for r in results])[len(results) // 2]

    max_Q_A = max(r["Q_A"] for r in results)
    max_Q_B = max(r["Q_B"] for r in results)
    max_Q_C = max(r["Q_C"] for r in results)

    conjecture_holds = median_Q_C >= 1.5 * median_Q_B and max_Q_A < n_values[0] ** (1/4)
    counterexample = ""

    if not conjecture_holds:
        if max_Q_B >= max_Q_C > max_Q_A - median_Q_A or any(Q(T_f_A) >= n**0.25 for n in n_values):
            counterexample = "median Q_C < 1.5 * median Q_B or max Q(A) >= n^{1/4}"

    return {
        "metric_name": "Q",
        "metric_value": (median_Q_A + median_Q_B + median_Q_C) / 3,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 60, 2))
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")

    Q_A_values = [r["Q_A"] for r in results]
    Q_B_values = [r["Q_B"] for r in results]
    Q_C_values = [r["Q_C"] for r in results]

    mean_Q_A = sum(Q_A_values) / len(Q_A_values)
    std_Q_A = math.sqrt(sum((x - mean_Q_A) ** 2 for x in Q_A_values) / len(Q_A_values))
    mean_Q_B = sum(Q_B_values) / len(Q_B_values)
    std_Q_B = math.sqrt(sum((x - mean_Q_B) ** 2 for x in Q_B_values) / len(Q_B_values))
    mean_Q_C = sum(Q_C_values) / len(Q_C_values)
    std_Q_C = math.sqrt(sum((x - mean_Q_C) ** 2 for x in Q_C_values) / len(Q_C_values))

    support_fraction_A = sum(1 for q in Q_A_values if q >= n_values[0] ** (1/4)) / len(Q_A_values)
    support_fraction_B = sum(1 for q in Q_B_values if q >= n_values[0] ** (1/4)) / len(Q_B_values)
    support_fraction_C = sum(1 for q in Q_C_values if q >= n_values[0] ** (1/4)) / len(Q_C_values)

    if all(support_fraction_A < 0.2 and support_fraction_B < 0.2 and support_fraction_C < 0.2):
        print(f"RESULT: SUPPORTED mean_Q_A={mean_Q_A} std_Q_A={std_Q_A} support_fraction_A={support_fraction_A}")
    elif any(support_fraction_A >= 0.2 or support_fraction_B >= 0.2 or support_fraction_C >= 0.2):
        print(f"RESULT: FALSIFIED counterexample=\"median Q_C < 1.5 * median Q_B or max Q(A) >= n^{1/4}\" first_failing_seed={seeds[0]}")
    else:
        print("RESULT: INCONCLUSIVE support_conditions_not_met")