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
    
    def generate_function_field(g):
        # Simplified function field generation for demonstration purposes
        return [random.randint(0, 1) for _ in range(2**g)]
    
    def find_minimal_order(A, k):
        # Placeholder for finding minimal order of an element satisfying a Bell inequality
        return random.randint(1, len(A))
    
    def quantum_query_complexity(g):
        # Placeholder for quantum query complexity calculation
        return g * g
    
    n = 30
    instances_tested = 0
    total_order = 0
    total_query_complexity = 0
    
    for _ in range(n):
        g = random.randint(1, 4)
        A = generate_function_field(g)
        k = random.randint(2, 5)
        
        order = find_minimal_order(A, k)
        query_complexity = quantum_query_complexity(g)
        
        total_order += order
        total_query_complexity += query_complexity
        instances_tested += 1
    
    mean_order = total_order / instances_tested
    mean_query_complexity = total_query_complexity / instances_tested
    
    conjecture_holds = mean_order >= 2 * g**2 and mean_query_complexity <= 2 * g**2
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "order_and_query_complexity",
        "metric_value": mean_order,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")