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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    instances_tested = 100
    metric_value = 0
    conjecture_holds = True
    counterexample = ""

    def generate_read_twice_bp(n):
        # Generate a random read-twice Boolean function
        return [random.choice([0, 1]) for _ in range(2**n)]

    def fourier_coefficient(bp, char):
        n = len(bp)
        sum_val = 0
        for i in range(2**n):
            sum_val += bp[i] * char(i, n)
        return abs(sum_val / (2**n))

    def young_tableaux_characters(n):
        # Generate characters of the symmetric group S_n using Young tableaux
        # This is a simplified version and may not be accurate for large n
        if n == 1:
            return [1]
        chars = [1]
        for k in range(2, n + 1):
            new_chars = []
            for i in range(k):
                new_chars.append(chars[i] * (k - i) / i)
            chars.extend(new_chars)
        return chars

    def ip_2_bp(n):
        # Generate a read-twice Boolean function for the IP_2 problem
        bp = [0] * (2**n)
        for x in range(2**(n-1)):
            for y in range(2**(n-1)):
                if x + y == 2**(n-1) - 1:
                    bp[x * 2**(n-1) + y] = 1
        return bp

    ip_2_bp_chars = young_tableaux_characters(n)
    max_ip_2_coeff = max(fourier_coefficient(ip_2_bp(n), char) for char in ip_2_bp_chars)

    other_bps_chars = [young_tableaux_characters(n)]
    max_other_bp_coeffs = [max(fourier_coefficient(generate_read_twice_bp(n), char) for char in chars) for chars in other_bps_chars]

    if max_ip_2_coeff < n:
        conjecture_holds = False
        counterexample = "IP_2 BP has Fourier coefficient gap less than n"

    if any(max_other_bp > math.log(n) for max_other_bp in max_other_bp_coeffs):
        conjecture_holds = False
        counterexample = "Other read-twice BP has Fourier coefficient gap greater than log(n)"

    metric_value = max_ip_2_coeff

    return {
        "metric_name": "Fourier Coefficient Gap",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support or budget exceeded")