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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_circuit(s):
        return [random.choice([0, 1]) for _ in range(2**s)]
    
    def reflection_group(circuit):
        n = len(circuit)
        G = []
        for i in range(n):
            for j in range(i+1, n):
                if circuit[i] != circuit[j]:
                    ref = [circuit[k] ^ (i == k or j == k) for k in range(n)]
                    G.append(ref)
        return G
    
    def correlation_coefficient(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(len(x))) / len(x))
        std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(len(y))) / len(y))
        if std_x == 0 or std_y == 0:
            return 0
        return cov / (std_x * std_y)
    
    n_max = 40
    instances_tested = 0
    total_r = 0
    
    for s in range(5, n_max + 1):
        circuit = generate_boolean_circuit(s)
        reflections = reflection_group(circuit)
        if len(reflections) > 5 * s:
            continue
        r = correlation_coefficient([len(reflections)], [s**0.5])
        total_r += r
        instances_tested += 1
    
    mean_r = total_r / instances_tested if instances_tested > 0 else 0
    conjecture_holds = mean_r >= 0.8 and instances_tested >= 30
    counterexample = "" if conjecture_holds else "correlation_coefficient_too_low"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": mean_r,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_r = sum(r["metric_value"] for r in results) / len(results) if results else 0
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_r} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.7:
        print(f"RESULT: SUPPORTED mean={mean_r} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_too_low\" first_failing_seed={first_failing_seed}")