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

def generate_circuit(n, depth):
    if n == 1 or depth == 0:
        return [random.choice([0, 1])]
    
    inputs = []
    for _ in range(2 ** (n - 1)):
        sub_inputs = generate_circuit(n // 2, depth - 1)
        inputs.append(sub_inputs[0] & sub_inputs[1])
    
    return inputs

def satisfiability_threshold(circuit):
    n = len(circuit)
    if n == 1:
        return circuit[0]
    
    threshold = 0
    for i in range(n):
        if circuit[i]:
            threshold += 2 ** (n - i - 1)
    
    return threshold

def p_adic_l_function_order(n, k):
    # Simplified approximation of the order of a p-adic L-function
    return n * math.log(k, 2)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Test with 5 different instances per size
            circuit = generate_circuit(n, random.randint(1, 3))
            k = satisfiability_threshold(circuit)
            order = p_adic_l_function_order(n, k)
            results.append((n, k, order))
    
    n_max = max(n for n, _, _ in results)
    if n_max < 16:
        return {
            "metric_name": "p-adic L-function order",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max < 16"
        }
    
    mean_order = sum(order for _, _, order in results) / len(results)
    std_dev = math.sqrt(sum((order - mean_order) ** 2 for _, _, order in results) / len(results))
    
    alpha, beta = random.random(), random.random()
    expected_bound = [alpha * math.log(n, 2) + beta for n, _, _ in results]
    
    conjecture_holds = all(abs(order - bound) <= 3 * std_dev for order, _, bound in zip(results, results, expected_bound))
    counterexample = "" if conjecture_holds else "order > alpha * log(n) + beta by more than 3 std deviations"
    
    return {
        "metric_name": "p-adic L-function order",
        "metric_value": mean_order,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    mean_order = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_order) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"order > alpha * log(n) + beta by more than 3 std deviations\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")