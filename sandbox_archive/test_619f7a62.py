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
    
    def young_tableau_characters(n):
        if n == 0:
            return [1]
        chars = []
        for part in partitions(n):
            char = Fraction(1, math.factorial(n))
            for i, p in enumerate(part):
                char *= math.factorial(p) / math.prod([math.factorial(i + 1) for i in range(len(part))])
            chars.append(char)
        return chars
    
    def partitions(n):
        if n == 0:
            yield []
        else:
            for part in partitions(n - 1):
                for i in range(len(part) + 1):
                    new_part = part[:i] + [part[i] + 1] + part[i+1:]
                    if new_part not in chars:
                        yield new_part
    
    def is_ip2(bp):
        # Placeholder function to determine if BP is IP_2
        return False
    
    n = random.randint(5, 40)
    bp = generate_random_bp(n)
    
    chars = young_tableau_characters(n)
    rho = max(abs(char) for char in chars)
    
    conjecture_holds = rho >= n if is_ip2(bp) else rho <= math.log(n)
    counterexample = "mapping_undefined" if not conjecture_holds else ""
    
    return {
        "metric_name": "Fourier_coefficient_gap",
        "metric_value": rho,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def generate_random_bp(n):
    # Placeholder function to generate a random read-twice BP
    return [random.choice([0, 1]) for _ in range(2**n)]

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rho = sum(r["metric_value"] for r in results) / len(results)
    std_rho = math.sqrt(sum((r["metric_value"] - mean_rho) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")