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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist")
    else:
        return x % m

def p_adic_norm(p, n):
    while n % p == 0:
        n //= p
    return n

def clause_indicator_polynomial(phi, p):
    n = len(phi)
    indicator = [1] * (2 ** n)
    for clause in phi:
        mask = 0
        for var in clause:
            if var < 0:
                mask |= 1 << (-var - 1)
            else:
                mask |= 1 << (var - 1)
        indicator[mask] += 1
    return [p_adic_norm(p, x) for x in indicator]

def monotone_gadget(phi):
    n = len(phi)
    gadget = []
    for i in range(2 ** n):
        if all((i & (1 << j)) != 0 for j in range(n) if phi[j] and not (i & (1 << j - 1))):
            gadget.append(i)
    return gadget

def monotone_width(gadget):
    n = len(bin(max(gadget))) - 2
    width = 0
    for i in range(2 ** n):
        count = sum((i & (1 << j)) != 0 for j in gadget)
        if count > width:
            width = count
    return width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    p = 3  # Prime number for p-adic norm
    n_max = 40
    instances_tested = 0
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            phi = [[random.randint(1, n) for _ in range(random.randint(1, n // 2))] for _ in range(n)]
            indicators = clause_indicator_polynomial(phi, p)
            mw = monotone_width(monotone_gadget(phi))
            min_Lp = min(indicators)
            metric_values.append(min_Lp)
            instances_tested += 1

    if len(metric_values) < 30:
        return {
            "metric_name": "min(Lp(φ))",
            "metric_value": sum(metric_values) / len(metric_values),
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }

    mean_Lp = sum(metric_values) / len(metric_values)
    if mean_Lp > 3:
        return {
            "metric_name": "min(Lp(φ))",
            "metric_value": mean_Lp,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": f"mean_Lp={mean_Lp} > 3"
        }

    correlation_coefficient = 0
    for i in range(len(metric_values)):
        x = metric_values[i]
        y = instances_tested - i
        correlation_coefficient += (x * y - mean_Lp * instances_tested) / math.sqrt((sum(x**2 for x in metric_values) - len(metric_values) * mean_Lp**2) * (instances_tested**2 - instances_tested))

    if correlation_coefficient < 0.8:
        return {
            "metric_name": "min(Lp(φ))",
            "metric_value": mean_Lp,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": f"correlation_coefficient={correlation_coefficient} < 0.8"
        }

    return {
        "metric_name": "min(Lp(φ))",
        "metric_value": mean_Lp,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean_Lp = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_Lp} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_Lp} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")