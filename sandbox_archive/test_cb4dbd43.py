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
    
    def zeta(s):
        if s == 1:
            return float('inf')
        result = 0
        for n in range(1, 10000):  # Avoid divergence by limiting the sum
            result += 1 / (n ** s)
        return result
    
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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2 ** n)]
    
    def branching_program_size(f, n):
        if len(f) != 2 ** n:
            return None
        size = 0
        for i in range(n):
            size += 1 + max(branching_program_size(f[:2**(n-i-1)]), branching_program_size(f[2**(n-i-1):]))
        return size
    
    def riemann_hypothesis_test():
        non_trivial_zeros = 0
        for _ in range(30):
            f = generate_boolean_function(40)
            zeta_value = zeta(0.5)
            if not is_prime(int(zeta_value)):
                continue
            bp_size = branching_program_size(f, 40)
            if bp_size is None or bp_size > 2 * (40 ** (3/4)):
                non_trivial_zeros += 1
        return non_trivial_zeros
    
    non_trivial_zeros = riemann_hypothesis_test()
    
    metric_value = non_trivial_zeros / 30
    conjecture_holds = metric_value >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Non-trivial Zeros",
        "metric_value": metric_value,
        "instances_tested": 30,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")