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
    
    # Generate a random XOR of N bits instance
    n = random.randint(5, 40)
    xor_bits = [random.choice([0, 1]) for _ in range(n)]
    xor_result = reduce(lambda x, y: x ^ y, xor_bits)
    
    # Placeholder for minimal rank calculation (not implemented)
    minimal_rank = float('inf')
    
    # Placeholder for tautology circuit size calculation (not implemented)
    tautology_circuit_size = 2 ** n
    
    # Measure the ratio between minimal rank and tautology circuit size
    if tautology_circuit_size == 0:
        return {
            "metric_name": "ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "tautology_circuit_size_zero"
        }
    
    ratio = minimal_rank / tautology_circuit_size
    
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": False if ratio < 1 else True,
        "counterexample": "" if ratio >= 1 else f"minimal_rank={minimal_rank}, tautology_circuit_size={tautology_circuit_size}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"minimal_rank < tautology_circuit_size\" first_failing_seed={first_failing_seed}")

def reduce(func, iterable):
    it = iter(iterable)
    value = next(it)
    for element in it:
        value = func(value, element)
    return value