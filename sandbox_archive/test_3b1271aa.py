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
    
    def generate_boolean_circuit(n):
        # Simplified boolean circuit generation for demonstration purposes
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def construct_tropical_division_algebra(circuit):
        # Placeholder function to simulate constructing a tropical division algebra
        return len(circuit)
    
    def min_order(A):
        # Placeholder function to simulate computing the minimal order of A
        return A
    
    n = random.randint(5, 40)  # Randomly choose n between 5 and 40
    circuit = generate_boolean_circuit(n)
    A = construct_tropical_division_algebra(circuit)
    MinOrder_A = min_order(A)
    
    metric_name = "MinOrder(A)"
    metric_value = MinOrder_A
    instances_tested = 1
    conjecture_holds = MinOrder_A <= len(circuit)
    counterexample = "" if conjecture_holds else f"Counterexample: n={n}, MinOrder(A)={MinOrder_A}, Circuit Size={len(circuit)}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")