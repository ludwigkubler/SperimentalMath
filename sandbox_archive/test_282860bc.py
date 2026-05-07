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
    
    def fast_walsh_hadamard_transform(f):
        n = len(f)
        if n == 1:
            return f
        even = fast_walsh_hadamard_transform([f[i] + f[i + n // 2] for i in range(n // 2)])
        odd = fast_walsh_hadamard_transform([f[i] - f[i + n // 2] for i in range(n // 2)])
        return [even[i] + odd[i] for i in range(n // 2)] + [even[i] - odd[i] for i in range(n // 2)]
    
    def sensitivity(f, n):
        max_sens = 0
        for i in range(n):
            sens = sum(abs(f[x] - f[toggle_bit(x, i)]) for x in range(1 << n) if x & (1 << i))
            max_sens = max(max_sens, sens)
        return max_sens
    
    def toggle_bit(x, i):
        return x ^ (1 << i)
    
    n = random.randint(5, 40)
    f = [random.choice([0, 1]) for _ in range(1 << n)]
    Fourier_coefficients = fast_walsh_hadamard_transform(f)
    max_Fourier_coefficient = max(abs(coeff) for coeff in Fourier_coefficients)
    sens = sensitivity(f, n)
    
    metric_name = "Fourier Coefficient Lower Bound"
    metric_value = max_Fourier_coefficient
    instances_tested = 1
    conjecture_holds = max_Fourier_coefficient >= sens / math.sqrt(n)
    counterexample = "" if conjecture_holds else f"n={n}, sensitivity={sens}, max_Fourier_coefficient={max_Fourier_coefficient}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")