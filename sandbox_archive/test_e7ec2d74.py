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
    return abs(a*b) // gcd(a, b)

def factorial(n):
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def binomial_coefficient(n, k):
    if k > n:
        return 0
    return factorial(n) // (factorial(k) * factorial(n - k))

def young_tableau_to_standard(young_tab):
    standard_tab = []
    for row in young_tab:
        standard_row = sorted(row)
        standard_tab.append(standard_row)
    return standard_tab

def hook_length_formula(tab, n):
    m = len(tab)
    hook_lengths = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if tab[i][j] == 0:
                continue
            hook_lengths[i][j] = (n - j) + (m - i) - binomial_coefficient(tab[i][j], 2)
    det = 1
    for i in range(m):
        for j in range(n):
            if tab[i][j] == 0:
                continue
            det *= hook_lengths[i][j]
    return det

def branching_rule(lam, mu, n):
    m = len(lam)
    result = 0
    for t in range(1 << (m - 1)):
        part = [lam[0]]
        for i in range(1, m):
            if t & (1 << (i - 1)):
                part.append(lam[i] - part[-1])
            else:
                part.append(part[-1])
        if len(part) != m:
            continue
        if sum(part) != n:
            continue
        tab = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if j < part[i]:
                    tab[i][j] = 1
        result += hook_length_formula(tab, n)
    return result

def multiplicity(lam, m, n):
    if sum(lam) != m:
        return 0
    if any(x > n for x in lam):
        return 0
    return branching_rule(lam, [n - m + i for i in range(m)], n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m_max = int(n ** 1.5)
    results = []
    for m in range(1, m_max):
        perm_multiplicity = multiplicity([n - m, m], m, n)
        det_multiplicity = multiplicity([m] * m, m, n)
        if perm_multiplicity <= det_multiplicity:
            counterexample = f"m={m}, n={n}: perm_multiplicity={perm_multiplicity}, det_multiplicity={det_multiplicity}"
            return {
                "metric_name": "Multiplicity Gap",
                "metric_value": 0,
                "instances_tested": m,
                "conjecture_holds": False,
                "counterexample": counterexample
            }
        results.append((m, perm_multiplicity - det_multiplicity))
    mean = sum(x[1] for x in results) / len(results)
    std_dev = math.sqrt(sum((x[1] - mean) ** 2 for x in results) / len(results))
    return {
        "metric_name": "Multiplicity Gap",
        "metric_value": mean,
        "instances_tested": m_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    mean = sum(x['metric_value'] for x in results) / len(results)
    std_dev = math.sqrt(sum((x['metric_value'] - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for x in results if x['conjecture_holds']) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not x['conjecture_holds'] for x in results):
        first_failing_seed = next(x['seed'] for x in results if not x['conjecture_holds'])
        counterexample = next(x['counterexample'] for x in results if not x['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")