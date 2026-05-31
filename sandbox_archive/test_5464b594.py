# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    K_2 = (Fraction(1, 2)) ** 0.5  # Corrected sqrt method for Fraction
    Khinchin_bound = lambda n: K_2 ** (n - 1)
    
    def communication_complexity(f):
        n = len(f)
        if n == 1:
            return 1
        count = 0
        for i in range(2**n):
            x = [bool(i >> j & 1) for j in range(n)]
            y = f(x)
            if y != f([not xi for xi in x]):
                count += 1
        return count / (2**(n-1))
    
    def generate_boolean_function(n):
        return lambda x: random.choice([True, False])
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = generate_boolean_function(n)
        CC_f = communication_complexity(f)
        Khinchin_value = Khinchin_bound(n)
        ratio = CC_f / Khinchin_value
        results.append({
            "n": n,
            "CC_f": CC_f,
            "Khinchin_value": Khinchin_value,
            "ratio": ratio
        })
    
    mean_ratio = sum(result["ratio"] for result in results) / len(results)
    std_ratio = (sum((result["ratio"] - mean_ratio) ** 2 for result in results) / len(results)) ** 0.5
    
    conjecture_holds = all(0.95 <= ratio <= 1.05 for result in results)
    
    return {
        "metric_name": "Communication Complexity Ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "Ratio out of ±5% range"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    std_ratio = (sum((result["metric_value"] - mean_ratio) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio out of ±5% range\" first_failing_seed={first_failing_seed}")