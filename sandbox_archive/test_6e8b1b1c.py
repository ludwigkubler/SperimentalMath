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
    
    def generate_boolean_circuit(s):
        return [random.choice([0, 1]) for _ in range(2**s)]
    
    def reflection_group(circuit):
        n = len(circuit)
        G = set()
        for i in range(n):
            for j in range(i+1, n):
                if circuit[i] != circuit[j]:
                    g = [circuit[k] ^ (i < k < j) for k in range(n)]
                    G.add(tuple(g))
        return G
    
    def correlation_coefficient(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x)))
        std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(len(x))) / len(x))
        std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(len(y))) / len(y))
        return cov / (std_x * std_y)
    
    n_max = 0
    instances_tested = 0
    total_r = 0
    max_reflections = 0
    
    for s in [5, 10, 15, 20, 30, 40]:
        if s > n_max:
            n_max = s
        
        for _ in range(5):
            circuit = generate_boolean_circuit(s)
            G = reflection_group(circuit)
            reflections = len(G)
            instances_tested += 1
            total_r += correlation_coefficient([reflections], [s**0.5])
            if reflections > max_reflections:
                max_reflections = reflections
    
    mean_r = total_r / instances_tested
    conjecture_holds = mean_r >= 0.8 and max_reflections <= 5 * n_max
    counterexample = "" if conjecture_holds else f"max_reflections={max_reflections}, n_max={n_max}"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": mean_r,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_r = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.7:
        print(f"RESULT: SUPPORTED mean={mean_r} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")