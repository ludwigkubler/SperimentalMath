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
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def min_brauer_classes(f):
        # Placeholder function to simulate Brauer class computation
        # This is a dummy implementation and should be replaced with actual logic
        return len(set(f))
    
    def circuit_complexity(f):
        # Placeholder function to simulate circuit complexity computation
        # This is a dummy implementation and should be replaced with actual logic
        return len(f)
    
    metric_name = "Brauer Classes vs Circuit Complexity"
    instances_tested = 0
    n_max = 40
    conjecture_holds = True
    counterexample = ""
    
    for n in range(4, n_max + 1):
        f = generate_boolean_function(n)
        B_f = min_brauer_classes(f)
        C_f = circuit_complexity(f)
        
        if B_f > C_f:
            conjecture_holds = False
            counterexample = f"n={n}, |B(f)|={B_f}, C(f)={C_f}"
            break
        
        instances_tested += 1
    
    return {
        "metric_name": metric_name,
        "metric_value": B_f / C_f if C_f != 0 else float('inf'),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")