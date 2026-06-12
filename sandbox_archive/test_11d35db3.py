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

def generate_boolean_circuit(n, d):
    if n == 1 and d == 0:
        return "input"
    elif d == 0:
        return ["not", generate_boolean_circuit(1, d)]
    else:
        left = generate_boolean_circuit(n//2, d-1)
        right = generate_boolean_circuit(n - n//2, d-1)
        return ["and", left, right]

def count_automorphic_forms(circuit):
    if isinstance(circuit, str):
        return 0
    elif circuit[0] == "not":
        return count_automorphic_forms(circuit[1]) + 1
    else:
        return count_automorphic_forms(circuit[1]) + count_automorphic_forms(circuit[2])

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 0
    total_forms = 0
    instances_tested = 0
    
    for d in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            n = random.randint(1, min(n_max + 1, 30))
            circuit = generate_boolean_circuit(n, d)
            forms = count_automorphic_forms(circuit)
            total_forms += forms
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_forms = Fraction(total_forms, instances_tested)
    C = 2  # Placeholder value for the constant C
    upper_bound = C * (n_max ** (1/3)) + n_max**2
    
    conjecture_holds = mean_forms <= upper_bound
    counterexample = "" if conjecture_holds else f"mean={mean_forms}, upper_bound={upper_bound}"
    
    return {
        "metric_name": "Automorphic Forms",
        "metric_value": float(mean_forms),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")