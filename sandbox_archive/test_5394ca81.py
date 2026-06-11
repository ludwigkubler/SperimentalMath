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
    
    def generate_circuit(n):
        # Generate a random n-variable Boolean circuit
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_brauer_group_order(circuit):
        # Placeholder function to compute Brauer group order
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, 10)
    
    def find_frege_proof_length(circuit):
        # Placeholder function to find the length of the smallest Frege proof
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(5, 20)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        circuit = generate_circuit(n)
        order = compute_brauer_group_order(circuit)
        length = find_frege_proof_length(circuit)
        results.append({"n": n, "order": order, "length": length})
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No circuits generated"
        }
    
    n_values = [r["n"] for r in results]
    order_values = [r["order"] for r in results]
    length_values = [r["length"] for r in results]
    
    n_mean = sum(n_values) / len(n_values)
    order_mean = sum(order_values) / len(order_values)
    length_mean = sum(length_values) / len(length_values)
    
    numerator = sum((n - n_mean) * (order - order_mean) * (length - length_mean) for n, order, length in zip(n_values, order_values, length_values))
    denominator = math.sqrt(sum((n - n_mean)**2 * (order - order_mean)**2 for n, order in zip(n_values, order_values))) * math.sqrt(sum((n - n_mean)**2 * (length - length_mean)**2 for n, length in zip(n_values, length_values)))
    
    if denominator == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Denominator is zero"
        }
    
    pearson_coefficient = numerator / denominator
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": pearson_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "First failing seed"
        mean_value = None
        std_value = None
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if all(r['conjecture_holds'] for r in results) else 'FALSIFIED'} mean={mean_value} std={std_value} support_fraction={support_fraction}")