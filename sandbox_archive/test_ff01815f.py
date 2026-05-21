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
    
    def fast_walsh_hadamard_transform(x):
        n = len(x)
        if n == 1:
            return x
        even = fast_walsh_hadamard_transform(x[0::2])
        odd = fast_walsh_hadamard_transform(x[1::2])
        result = [0] * n
        for i in range(n // 2):
            result[i] = even[i] + odd[i]
            result[i + n // 2] = even[i] - odd[i]
        return result
    
    def additive_energy(coeffs):
        n = len(coeffs)
        energy = 0
        for i in range(n):
            for j in range(i + 1, n):
                if coeffs[i] * coeffs[j] != 0:
                    energy += 1
        return energy
    
    def sipser_function(n, x):
        result = 0
        for i in range(n):
            result ^= x[i]
        return result
    
    n = random.randint(5, 40)
    x = [random.randint(0, 1) for _ in range(n)]
    coeffs = fast_walsh_hadamard_transform([sipser_function(n, x[:i] + (x[i] ^ 1,) + x[i+1:]) for i in range(n)])
    energy = additive_energy(coeffs)
    
    return {
        "metric_name": "additive_energy",
        "metric_value": energy,
        "instances_tested": 1,
        "conjecture_holds": energy >= 2 ** (n / 2),
        "counterexample": "" if energy >= 2 ** (n / 2) else f"Graph with n={n}, coeffs={coeffs}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_energy = sum(res["metric_value"] for res in results) / len(results)
    std_energy = math.sqrt(sum((res["metric_value"] - mean_energy) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_energy} std={std_energy} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")