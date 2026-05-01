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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def additivity(f):
        n = int(math.log2(len(f)))
        count = 0
        for i in range(n):
            for j in range(i+1, n):
                for k in range(j+1, n):
                    if f[i] + f[j] == f[k]:
                        count += 1
        return count
    
    def additive_energy(f):
        n = int(math.log2(len(f)))
        return additivity(f) / (n * (n - 1) * (n - 2))
    
    def acc0_circuit_size_bound(n, epsilon):
        return n ** (1 + epsilon)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_boolean_function(n)
    energy = additive_energy(f)
    epsilon = 0.1
    conjecture_holds = energy >= n ** (2 - epsilon) and acc0_circuit_size_bound(n, epsilon) <= n ** (1 + epsilon)
    
    return {
        "metric_name": "additive_energy",
        "metric_value": energy,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Energy {energy} < n^(2-{epsilon}) for n={n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_energy = sum(r["metric_value"] for r in results) / len(results)
    std_energy = math.sqrt(sum((r["metric_value"] - mean_energy) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_energy} std={std_energy} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")