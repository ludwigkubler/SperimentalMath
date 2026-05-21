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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_convex_polytope(f):
        # Placeholder function to simulate convex polytope computation
        # This is a dummy implementation and should be replaced with actual logic
        return random.random()
    
    def compute_intersection_body(polytope):
        # Placeholder function to simulate intersection body computation
        # This is a dummy implementation and should be replaced with actual logic
        return polytope ** 2
    
    def compute_acc0_circuit(f):
        # Placeholder function to simulate ACC⁰ parity circuit computation
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, 10)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_function(n)
    polytope = compute_convex_polytope(f)
    intersection_body = compute_intersection_body(polytope)
    acc0_circuit_size = compute_acc0_circuit(f)
    
    if acc0_circuit_size == 0:
        return {
            "metric_name": "Vol(IntersectionBody(f)) / ACC⁰(f)",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "acc0_circuit_size_zero"
        }
    
    ratio = Fraction(intersection_body, acc0_circuit_size)
    support_fraction = abs(1 - ratio)
    
    return {
        "metric_name": "Vol(IntersectionBody(f)) / ACC⁰(f)",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": support_fraction <= 0.1,
        "counterexample": "" if support_fraction <= 0.1 else f"support_fraction={support_fraction}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std_dev = (sum((r["metric_value"] - mean) ** 2 for r in results) / len(results)) ** 0.5
        support_fraction = sum(1 for r in results if abs(1 - r["metric_value"]) <= 0.1) / len(results)
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction_exceeds_0.1\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")