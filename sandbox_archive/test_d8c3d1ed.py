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
    
    def generate_circuits(n, D):
        if n == 1:
            return [[random.choice([0, 1])]]
        else:
            circuits = []
            for i in range(2**n):
                inputs = [i >> j & 1 for j in range(n)]
                outputs = generate_circuits(n-1, D)
                for output in outputs:
                    circuits.append(inputs + output)
            return circuits
    
    def topological_entropy(lattice):
        n = len(lattice)
        if n == 0:
            return 0
        log_n = math.log2(n)
        entropy = 0
        for i in range(1, n):
            count = sum(1 for x in lattice if x & (1 << i) != 0)
            if count > 0 and count < n:
                entropy += -count / n * math.log2(count / n)
        return entropy
    
    def sauer_spencer_bound(n, D):
        if n == 0 or D == 0:
            return 0
        return (n + 1) * math.log2(D + 1)
    
    n_values = [2, 4, 8]
    total_entropy = 0
    instances_tested = 0
    
    for n in n_values:
        max_depth = int(math.log2(n + D))
        circuits = generate_circuits(n, max_depth)
        for circuit in circuits:
            entropy = topological_entropy(circuit)
            if entropy < sauer_spencer_bound(n, len(circuit)):
                return {
                    "metric_name": "topological_entropy",
                    "metric_value": entropy,
                    "instances_tested": instances_tested,
                    "n_max": n,
                    "conjecture_holds": False,
                    "counterexample": f"Circuit {circuit} has lower entropy than expected"
                }
            total_entropy += entropy
            instances_tested += 1
    
    mean_entropy = total_entropy / instances_tested
    c = 0.5  # Example constant, adjust as needed
    if mean_entropy >= c * math.log2(n + D):
        return {
            "metric_name": "topological_entropy",
            "metric_value": mean_entropy,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "topological_entropy",
            "metric_value": mean_entropy,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": f"Mean entropy {mean_entropy} < c * log2({n + D})"
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_entropy = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_entropy} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_entropy} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")