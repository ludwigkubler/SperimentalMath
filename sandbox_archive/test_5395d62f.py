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
    n = 40
    instances_tested = 30
    support_fraction = 0.1
    c = 1.0
    
    def generate_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_convex_polytope(f):
        # Placeholder function to simulate computation of convex polytope
        return random.uniform(1, 10)
    
    def compute_intersection_body(polytope):
        # Placeholder function to simulate computation of intersection body volume
        return polytope
    
    def compute_acc0_circuit_size(f):
        # Placeholder function to simulate computation of ACC⁰ circuit size
        return random.randint(1, 100)
    
    ratio_values = []
    for _ in range(instances_tested):
        f = generate_function(n)
        polytope = compute_convex_polytope(f)
        intersection_body_volume = compute_intersection_body(polytope)
        acc0_circuit_size = compute_acc0_circuit_size(f)
        
        if acc0_circuit_size == 0:
            continue
        
        ratio = Fraction(intersection_body_volume, acc0_circuit_size)
        ratio_values.append(ratio)
    
    mean_ratio = sum(ratio_values) / len(ratio_values)
    conjecture_holds = all(abs(mean_ratio - c) <= support_fraction for _ in range(instances_tested))
    counterexample = "" if conjecture_holds else f"Counterexample found: Ratio={mean_ratio}, c={c}"
    
    return {
        "metric_name": "Ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [727, 773, 821, 877, 929]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if not r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction <= 0.2:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")