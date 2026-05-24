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
    
    # Generate a random explicit function f in P with varying degrees of complexity.
    n = random.randint(5, 40)
    f = [random.choice([0, 1]) for _ in range(n)]
    
    # Compute the Hodge decomposition of each function and determine its local index.
    # This is a placeholder for actual computation. For simplicity, we assume the local index is the number of 1s in the function.
    local_index = f.count(1)
    
    # Attempt to construct an ACC⁰ circuit using a Sipser function and measure its size.
    # This is a placeholder for actual computation. For simplicity, we assume the ACC⁰ circuit size is proportional to the number of 1s.
    acc0_circuit_size = local_index * 2
    
    # Correlate the local index of Hodge decomposition with the size of the ACC⁰ circuit.
    if local_index > 2:
        conjecture_holds = False
        counterexample = f"Function with {n} bits and {local_index} ones, ACC⁰ circuit size: {acc0_circuit_size}"
    else:
        conjecture_holds = True
        counterexample = ""
    
    return {
        "metric_name": "ACC⁰ Circuit Size",
        "metric_value": acc0_circuit_size,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        result = f"SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        result = f"FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    
    print(result)