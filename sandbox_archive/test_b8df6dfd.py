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
    
    def frege_proof_length(f):
        n = len(f)
        if n == 1:
            return 1
        else:
            return 1 + max(frege_proof_length(f[:n//2]), frege_proof_length(f[n//2:]))
    
    def riemann_surface_area(n):
        # Simplified approximation for demonstration purposes
        return n * math.log2(n)
    
    metric_name = "FregeProofLength"
    instances_tested = 0
    total_area = 0
    total_length = 0
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        length = frege_proof_length(f)
        area = riemann_surface_area(n)
        
        total_area += area
        total_length += length
        instances_tested += 1
    
    mean_area = total_area / instances_tested
    mean_length = total_length / instances_tested
    correlation_coefficient = (instances_tested * sum(area * length for area, length in zip([riemann_surface_area(n) for n in [5, 10, 15, 20, 30, 40]], [frege_proof_length(generate_boolean_function(n)) for n in [5, 10, 15, 20, 30, 40]])) - instances_tested * mean_area * mean_length) / (instances_tested * sum((area - mean_area)**2 for area in [riemann_surface_area(n) for n in [5, 10, 15, 20, 30, 40]]) * sum((length - mean_length)**2 for length in [frege_proof_length(generate_boolean_function(n)) for n in [5, 10, 15, 20, 30, 40]]))
    
    conjecture_holds = correlation_coefficient >= 0.8 and abs(mean_area - mean_length) <= 3
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max([5, 10, 15, 20, 30, 40]),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")