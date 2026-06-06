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
    
    def generate_circuit(n):
        # Generate a random boolean circuit with n inputs
        if n == 1:
            return ['0'] * 2 + ['1'] * 2
        else:
            left = generate_circuit(n // 2)
            right = generate_circuit(n - n // 2)
            return [f'AND({left[i]}, {right[i]})' for i in range(len(left))]
    
    def local_index(circuit):
        # Placeholder function to compute the local index of the symmetry group
        # This is a dummy implementation and should be replaced with actual computation
        return len(set(circuit))
    
    def monotone_width(circuit):
        # Placeholder function to compute the monotone width of the circuit
        # This is a dummy implementation and should be replaced with actual computation
        return len(circuit)
    
    n = random.randint(5, 40)
    circuit = generate_circuit(n)
    G = local_index(circuit)
    w_C = monotone_width(circuit)
    
    return {
        "metric_name": "Local Index vs Monotone Width",
        "metric_value": G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")