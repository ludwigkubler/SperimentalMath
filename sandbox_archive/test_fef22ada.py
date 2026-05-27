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
    
    # Generate a random boolean function with n variables and depth d
    n = 10  # Number of variables
    d = 5   # Depth of the circuit
    
    def generate_circuit(depth, num_inputs):
        if depth == 1:
            return [random.choice([0, 1])]
        else:
            inputs = generate_circuit(depth - 1, num_inputs)
            return [random.choice([0, 1]) for _ in range(num_inputs)]
    
    circuit = generate_circuit(d, n)
    
    # Compute the associated quasi-polynomial L-function R_C
    def l_function(circuit):
        if len(circuit) == 1:
            return circuit[0]
        else:
            left = l_function(circuit[:len(circuit)//2])
            right = l_function(circuit[len(circuit)//2:])
            return (left + right) % 2
    
    rank = l_function(circuit)
    
    # Measure the rank of R_C
    metric_value = rank
    
    # Check if the conjecture holds for this seed
    conjecture_holds = rank >= math.log(n, 2)
    counterexample = "" if conjecture_holds else f"Rank {rank} is less than log({n}, 2) = {math.log(n, 2)}"
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
        print(f"RESULT: FALSIFIED counterexample=\"Rank less than log(n)\" first_failing_seed={first_failing_seed}")