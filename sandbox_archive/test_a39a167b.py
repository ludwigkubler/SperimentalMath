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

def noncommutative_fourier_transform(f):
    n = len(f)
    transform = [0] * (1 << n)
    for j in range(1 << n):
        term = 0
        for i in range(n):
            if j & (1 << i):
                term += f[i]
            else:
                term -= f[i]
        transform[j] = Fraction(term, 2 ** n)
    return transform

def communication_complexity(f):
    n = len(f)
    max_cc = 0
    for x in range(1 << n):
        for y in range(1 << n):
            cc = 0
            for i in range(n):
                if (x & (1 << i)) != (y & (1 << i)):
                    cc += 1
            max_cc = max(max_cc, cc)
    return max_cc

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    f = [random.choice([0, 1]) for _ in range(n)]
    
    transform = noncommutative_fourier_transform(f)
    cc = communication_complexity(f)
    
    tau_p = sum(abs(x) ** p for x in transform) ** (1 / p)
    expected_cc = n ** (1 - p / k)
    
    correlation_coefficient = (tau_p - expected_cc) / (n ** (1 - p / k))
    
    conjecture_holds = abs(correlation_coefficient) > 0.9 and tau_p / n ** (1 - p / k) >= 0.8
    counterexample = "" if conjecture_holds else f"CC({f})"
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": correlation_coefficient,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean = sum(result["metric_value"] for result in results) / len(results)
    std = (sum((result["metric_value"] - mean) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")