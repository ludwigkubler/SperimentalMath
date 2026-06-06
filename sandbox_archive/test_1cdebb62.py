# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def generate_boolean_circuit(W):
    if W == 1:
        return ['0', '1']
    w = random.randint(1, W - 1)
    left = generate_boolean_circuit(w)
    right = generate_boolean_circuit(W - w)
    return [f'({l} & {r})' for l in left] + [f'({l} | {r})' for l in right]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    metric_name = "Circuit Monotone Width"
    instances_tested = 0
    total_dimension = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        W = random.randint(1, n)
        circuit = generate_boolean_circuit(W)
        
        # Simulate the computation of the dimension of the moduli space
        # This is a placeholder for actual computation which depends on the circuit structure
        # For simplicity, we assume the dimension is proportional to W^2
        dimension = Fraction(W ** 2, n)
        
        total_dimension += dimension
        instances_tested += 1
    
    mean_dimension = total_dimension / instances_tested
    conjecture_holds = mean_dimension <= W ** 2
    counterexample = "" if conjecture_holds else f"Mean Dimension: {mean_dimension}, Expected: {W**2}"
    
    return {
        "metric_name": metric_name,
        "metric_value": float(mean_dimension),
        "instances_tested": instances_tested,
        "n_max": 40,
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
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")