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

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_primes(n):
    primes = []
    for num in range(2, n):
        if is_prime(num):
            primes.append(num)
    return primes

def quadratic_residues(p):
    residues = set()
    for a in range(1, p):
        if gcd(a, p) == 1:
            residues.add((a * a) % p)
    return residues

def rank_quadratic_reciprocity_table_entry(p, a):
    if a % p == 0:
        return None
    q = (a * a) % p
    if q not in quadratic_residues(p):
        return None
    table = [[None] * p for _ in range(p)]
    for i in range(1, p):
        for j in range(1, p):
            table[i][j] = (i * j) % p
    row = [table[a][j] for j in range(1, p)]
    col = [table[i][a] for i in range(1, p)]
    rank = 0
    for r in row:
        if r is not None and r != 0:
            rank += 1
    for c in col:
        if c is not None and c != 0:
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            p = random.choice(generate_primes(n * 10))
            a = random.randint(1, p - 1)
            if gcd(a, p) != 1:
                continue
            rank = rank_quadratic_reciprocity_table_entry(p, a)
            if rank is None:
                conjecture_holds = False
                counterexample = "mapping_undefined"
                break
            metric_values.append(rank)
            instances_tested += 1

    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for v in metric_values if v >= 0.5 * math.log(2**(p-0.5))) / len(metric_values)

    return {
        "metric_name": "Rank of Quadratic Reciprocity Table Entry",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or generate_primes(30)
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data n_tested={len(results)}")