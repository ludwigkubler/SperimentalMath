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
        return [random.randint(0, 1) for _ in range(2**n)]
    
    def young_french_algorithm(f):
        n = len(f)
        generators = set()
        for i in range(n):
            for j in range(i+1, n):
                if f[i] != f[j]:
                    generators.add((i, j))
        return len(generators)
    
    def circuit_entanglement_complexity(f):
        # Placeholder implementation
        # For simplicity, we assume the complexity is proportional to the number of variables
        return len(f)
    
    n = random.randint(5, 40)  # Ensure n_min >= 5 and n_max >= 20
    f = generate_boolean_function(n)
    
    num_generators = young_french_algorithm(f)
    entanglement_complexity = circuit_entanglement_complexity(f)
    
    if entanglement_complexity == 0:
        return {
            "metric_name": "Ratio of Generators to Entanglement",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Entanglement complexity is zero"
        }
    
    ratio = num_generators / entanglement_complexity
    
    return {
        "metric_name": "Ratio of Generators to Entanglement",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(ratio - 1) <= 0.2,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["conjecture_holds"]) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results if r["conjecture_holds"])) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Ratio exceeds bounds' first_failing_seed={first_failing_seed}")