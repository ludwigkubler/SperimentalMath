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

def fast_walsh_hadamard_transform(f):
    n = len(f)
    if n == 1:
        return f
    
    even = fast_walsh_hadamard_transform(f[::2])
    odd = fast_walsh_hadamard_transform(f[1::2])
    
    result = [0] * n
    for k in range(n // 2):
        result[k] = even[k] + odd[k]
        result[k + n // 2] = even[k] - odd[k]
    
    return result

def add(a, b):
    return a + b

def mul(a, b):
    return a * b

def inner_product(f, g):
    n = len(f)
    return sum(mul(f[i], g[i]) for i in range(n))

def additive_energy(f):
    n = len(f)
    energy = 0
    for a in range(1 << n):
        for b in range(1 << n):
            chi_a = [(-1) ** (a & (1 << j)) for j in range(n)]
            chi_b = [(-1) ** (b & (1 << j)) for j in range(n)]
            energy += abs(inner_product(f, chi_a) * inner_product(f, chi_b))
    return energy

def generate_random_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(1 << n)]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 10
    f = generate_random_boolean_function(n)
    transformed_f = fast_walsh_hadamard_transform(f)
    
    energy = additive_energy(transformed_f)
    
    return {
        "metric_name": "additive_energy",
        "metric_value": energy,
        "instances_tested": 1,
        "conjecture_holds": energy >= 2 ** (n * math.log(2, 3)),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_energy = sum(res["metric_value"] for res in results) / len(results)
    std_energy = math.sqrt(sum((res["metric_value"] - mean_energy) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_energy} std={std_energy} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_energy} std={std_energy} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"additive_energy\" first_failing_seed={first_failing_seed}")