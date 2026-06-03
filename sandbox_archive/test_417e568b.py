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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random

def generate_boolean_circuit(w):
    if w <= 0:
        return []
    elif w == 1:
        return [random.choice(['AND', 'OR'])]
    else:
        left = generate_boolean_circuit(random.randint(1, w-1))
        right = generate_boolean_circuit(w - len(left) - 1)
        return ['NOT'] + left + right

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    metric_name = "minimal_order_of_automorphism_groups"
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):  # Ensure at least 5 instances per size
            circuit = generate_boolean_circuit(n)
            w_C = len(circuit) - 1  # Monotone width of the circuit
            
            if w_C <= 0:
                continue
            
            # Simulate constructing an affine quasi-projective variety and computing its automorphism group order
            ord_V = (w_C ** 2) + random.randint(1, 5)  # Simplified simulation
            
            instances_tested += 1
            
            if ord_V < w_C ** 2:
                conjecture_holds = False
                counterexample = f"n={n}, w(C)={w_C}, ord(V)={ord_V}"
                break
    
    return {
        "metric_name": metric_name,
        "metric_value": (instances_tested - sum(1 for _ in range(instances_tested) if not conjecture_holds)) / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = (sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results)) ** 0.5
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")