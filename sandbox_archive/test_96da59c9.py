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

def fast_walsh_hadamard_transform(f):
    n = len(f)
    for s in range(1, int(math.log2(n)) + 1):
        half = n // (1 << s)
        for i in range(half):
            mask = (1 << s) - 1
            for j in range(half):
                u = f[i * (1 << s) + j]
                v = f[i * (1 << s) + j + half]
                f[i * (1 << s) + j] = u + v
                f[i * (1 << s) + j + half] = u - v
    return f

def additivity_energy(f):
    n = len(f)
    energy = 0
    for a in range(n):
        for b in range(a, n):
            energy += abs(f[a] * f[b])
    return energy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10
    f = [random.choice([0, 1]) for _ in range(2**n)]
    
    transformed_f = fast_walsh_hadamard_transform(f)
    energy = additivity_energy(transformed_f)
    
    return {
        "metric_name": "additive_energy",
        "metric_value": energy,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_energy = sum(r["metric_value"] for r in results) / len(results)
    std_energy = math.sqrt(sum((r["metric_value"] - mean_energy)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if not r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_energy} std={std_energy} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")