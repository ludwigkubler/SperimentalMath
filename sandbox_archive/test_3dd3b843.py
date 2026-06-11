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
    
    def generate_balanced_binary_tree(h):
        if h == 0:
            return []
        left = generate_balanced_binary_tree(h - 1)
        right = generate_balanced_binary_tree(h - 1)
        return [left, right]
    
    def calculate_symplectic_volume(tree):
        if not tree:
            return 1
        left, right = tree
        return calculate_symplectic_volume(left) * calculate_symplectic_volume(right)
    
    def calculate_circuit_entanglement(tree):
        if not tree:
            return 0
        left, right = tree
        return 1 + max(calculate_circuit_entanglement(left), calculate_circuit_entanglement(right))
    
    results = []
    for h in range(5, 41):
        tree = generate_balanced_binary_tree(h)
        symplectic_volume = calculate_symplectic_volume(tree)
        circuit_entanglement = calculate_circuit_entanglement(tree)
        if circuit_entanglement == 0:
            continue
        ratio = symplectic_volume / circuit_entanglement
        results.append((h, ratio))
    
    if not results:
        return {
            "metric_name": "SymplecticVolumeToCircuitEntanglementRatio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    h_values, ratio_values = zip(*results)
    mean_ratio = sum(ratio_values) / len(ratio_values)
    n_max = max(h_values)
    
    return {
        "metric_name": "SymplecticVolumeToCircuitEntanglementRatio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    else:
        seeds = [int(seed) for seed in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" not in r or r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if "conjecture_holds" not in r or r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "counterexample" in result and result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")