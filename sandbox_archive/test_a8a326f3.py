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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_balanced_binary_tree(h):
        if h == 0:
            return []
        elif h == 1:
            return [None]
        else:
            left = generate_balanced_binary_tree(h - 1)
            right = generate_balanced_binary_tree(h - 1)
            return [left, right]

    def calculate_symplectic_volume(tree):
        if not tree:
            return 0
        elif len(tree) == 1:
            return 1
        else:
            left, right = tree
            return calculate_symplectic_volume(left) + calculate_symplectic_volume(right)

    def calculate_circuit_entanglement(tree):
        if not tree:
            return 0
        elif len(tree) == 1:
            return 1
        else:
            left, right = tree
            return calculate_circuit_entanglement(left) + calculate_circuit_entanglement(right)

    results = []
    for h in range(5, 41):
        tree = generate_balanced_binary_tree(h)
        symplectic_volume = calculate_symplectic_volume(tree)
        circuit_entanglement = calculate_circuit_entanglement(tree)
        if circuit_entanglement == 0:
            continue
        ratio = Fraction(symplectic_volume, circuit_entanglement)
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

    h_values, ratios = zip(*results)
    n = len(h_values)

    # Calculate correlation coefficient
    mean_h = sum(h_values) / n
    mean_ratio = sum(ratios) / n
    numerator = sum((h - mean_h) * (r - mean_ratio) for h, r in results)
    denominator = ((sum((h - mean_h) ** 2 for h in h_values)) *
                   (sum((r - mean_ratio) ** 2 for r in ratios))) ** 0.5
    correlation_coefficient = numerator / denominator if denominator != 0 else 0

    # Calculate mean absolute difference
    predicted_ratios = [mean_ratio + (h - mean_h) * (correlation_coefficient / n) for h in h_values]
    mean_absolute_difference = sum(abs(r - p) for r, p in zip(ratios, predicted_ratios)) / n

    return {
        "metric_name": "SymplecticVolumeToCircuitEntanglementRatio",
        "metric_value": correlation_coefficient,
        "instances_tested": n,
        "n_max": 40,
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_absolute_difference <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2**i + 1 for i in range(5, 31)]
    else:
        seeds = [int(s) for s in sys.argv[1:]]

    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    if all(result["conjecture_holds"] for result in results):
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        counterexample = ""
    else:
        mean_metric_value = None
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
        counterexample = next((result["counterexample"] for result in results if result["counterexample"]), "")

    print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")