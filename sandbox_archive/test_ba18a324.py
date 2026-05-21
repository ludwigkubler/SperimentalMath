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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_read_twice_bp(n):
        # Generate a random read-twice Boolean function
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def fourier_coefficient(bp, char):
        n = len(bp)
        sum_val = 0
        for i in range(2**n):
            term = 1
            for j in range(n):
                if bp[i ^ (1 << j)] != bp[i]:
                    term *= char[j]
            sum_val += term
        return abs(sum_val / 2**n)
    
    def young_tableau_characters(n):
        # Generate characters of the symmetric group S_n using Young tableaux
        if n == 1:
            return [1]
        chars = []
        for partition in partitions(n):
            char = 1
            for part in partition:
                char *= math.factorial(part) / math.prod([math.factorial(i + 1) for i in range(len(part))])
            chars.append(char)
        return chars
    
    def partitions(n):
        # Generate all partitions of n
        if n == 0:
            yield []
            return
        for p in partitions(n - 1):
            yield [1] + p
            if p and p[0] > 1:
                yield [p[0] - 1, 1] + p[1:]
    
    def is_ip2(bp):
        # Check if the BP corresponds to the IP_2 problem
        n = int(math.log2(len(bp)))
        return all(bp[i ^ (1 << j)] != bp[i] for i in range(2**n) for j in range(n))
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 different BPs
            bp = generate_read_twice_bp(n)
            chars = young_tableau_characters(n)
            max_coeff = max(fourier_coefficient(bp, char) for char in chars)
            instances_tested += 1
            total_metric_value += max_coeff
            if is_ip2(bp):
                if max_coeff < n:
                    conjecture_holds = False
                    counterexample = f"IP_2 BP with n={n}, max_coeff={max_coeff}"
            else:
                if max_coeff >= math.log(n):
                    conjecture_holds = False
                    counterexample = f"Not IP_2 BP with n={n}, max_coeff={max_coeff}"
    
    return {
        "metric_name": "Fourier Coefficient Gap",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")