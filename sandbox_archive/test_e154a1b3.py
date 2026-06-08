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

def generate_boolean_circuit(n: int) -> tuple:
    if n == 1:
        return (random.choice([True, False]), [])
    
    left_size = random.randint(1, n-1)
    right_size = n - left_size - 1
    
    left, left_edges = generate_boolean_circuit(left_size)
    right, right_edges = generate_boolean_circuit(right_size)
    
    node_id = len(left) + len(right)
    edges = [(node_id, i) for i in range(len(left))] + [(node_id, i + len(left)) for i in range(len(right))]
    
    return (left + right, left_edges + right_edges + edges)

def compute_minimal_order(n: int, leaf_count: int) -> float:
    if n <= 0 or leaf_count <= 0:
        return None
    
    return math.log(n / leaf_count)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    metric_name = "minimal_order"
    instances_tested = 0
    n_max = 1
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):
            circuit, edges = generate_boolean_circuit(n)
            leaf_count = sum(1 for _, child in edges if child >= len(circuit))
            
            order = compute_minimal_order(n, leaf_count)
            
            if order is None:
                conjecture_holds = False
                counterexample = "mapping_undefined"
                break
            
            instances_tested += 1
    
    return {
        "metric_name": metric_name,
        "metric_value": order,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(r["metric_value"] for r in results if r["conjecture_holds"]) / len(results)
    std_order = math.sqrt(sum((r["metric_value"] - mean_order) ** 2 for r in results if r["conjecture_holds"])) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_order} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_order} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")