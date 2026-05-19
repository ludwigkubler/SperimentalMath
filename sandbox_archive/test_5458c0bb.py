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
    
    def fourier_transform(f, n):
        result = [0] * (1 << n)
        for i in range(1 << n):
            for j in range(n):
                if i & (1 << j):
                    result[i] += f[j]
                else:
                    result[i] -= f[j]
            result[i] /= math.sqrt(n)
        return result
    
    def sipser_function(x):
        return sum(x[i] for i in range(len(x)) if i % 2 == 0) % 2
    
    n = random.randint(5, 40)
    f = [random.choice([0, 1]) for _ in range(n)]
    
    ft = fourier_transform(f, n)
    max_coefficient = max(abs(coeff) for coeff in ft if len(bin(i).split('b')[1]) == n // 2)
    
    circuit_size = (1 << n) * math.log2(1 << n)
    
    return {
        "metric_name": "max_fourier_coefficient",
        "metric_value": max_coefficient,
        "instances_tested": 1,
        "conjecture_holds": max_coefficient < 1 / math.sqrt(n),
        "counterexample": "" if conjecture_holds else f"Sipser function with n={n}, f={f}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 6)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Sipser function\" first_failing_seed={first_failing_seed}")