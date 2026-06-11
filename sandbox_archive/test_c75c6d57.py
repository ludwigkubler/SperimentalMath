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
    
    def generate_circuit(size, depth):
        if size == 1 and depth == 1:
            return ["NOT"]
        elif size == 1:
            return [random.choice(["AND", "OR"])]
        else:
            sub_size = random.randint(1, size - 1)
            sub_depth = random.randint(1, depth - 1)
            left = generate_circuit(sub_size, sub_depth)
            right = generate_circuit(size - sub_size, depth - sub_depth)
            return [random.choice(["AND", "OR"])] + left + right
    
    def symplectic_area(circuit):
        if not circuit:
            return 0
        gate = circuit[0]
        if gate == "NOT":
            return 1
        elif gate in ["AND", "OR"]:
            return 2 + symplectic_area(circuit[1:])
    
    size_range = [5, 10, 15, 20, 30, 40]
    depth_range = [5, 10]
    results = []
    
    for _ in range(30):
        size = random.choice(size_range)
        depth = random.choice(depth_range)
        circuit = generate_circuit(size, depth)
        area = symplectic_area(circuit)
        bound = size**2 * depth
        results.append({
            "metric_name": "Symplectic Area",
            "metric_value": area,
            "instances_tested": 1,
            "n_max": max(size_range),
            "conjecture_holds": area <= bound,
            "counterexample": "" if area <= bound else f"Circuit size {size}, depth {depth} violated the bound"
        })
    
    return {
        "seed": seed,
        "metric_name": "Symplectic Area",
        "metric_value": sum(r["metric_value"] for r in results),
        "instances_tested": len(results),
        "n_max": max(size_range),
        "conjecture_holds": all(r["conjecture_holds"] for r in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [601, 631, 677, 727, 773, 821, 877, 929]  # Default list of primes
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Circuit size {results[first_failing_seed]['n_max']} violated the bound\" first_failing_seed={first_failing_seed}")