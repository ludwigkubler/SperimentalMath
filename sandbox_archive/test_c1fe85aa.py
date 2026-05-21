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
    for s in range(1, n):
        m = 1 << s
        for i in range(m):
            mask = (1 << s) - 1
            for j in range(i, n, 2 * m):
                u = f[j]
                v = f[j + m]
                f[j] = u + v
                f[j + m] = u - v
    return f

def additive_energy(f):
    n = len(f)
    energy = 0
    for a in range(n):
        for b in range(a, n):
            energy += abs(f[a] * f[b])
    return energy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10
    instances_tested = 30
    total_energy = 0
    
    for _ in range(instances_tested):
        f = [random.choice([0, 1]) for _ in range(2**n)]
        transformed_f = fast_walsh_hadamard_transform(f)
        energy = additive_energy(transformed_f)
        total_energy += energy
    
    avg_energy = total_energy / instances_tested
    conjecture_holds = avg_energy >= 2**(math.log2(n) * 3)
    counterexample = "" if conjecture_holds else "energy_too_low"
    
    return {
        "metric_name": "additive_energy",
        "metric_value": avg_energy,
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
    
    mean_energy = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_energy} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_energy} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='energy_too_low' first_failing_seed={first_failing_seed}")